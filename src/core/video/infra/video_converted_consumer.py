import json
from uuid import UUID
from venv import logger
import pika
from src._shared.logger import get_logger
from src.core._shared.events.abstract_consumer import AbstractConsumer
from src.core.video.application.use_cases.process_audio_video_media import ProcessAudioVideoMedia, ProcessAudioVideoMediaInput
from src.core.video.domain.value_objetcs import MediaStatus
from src.core.video.infra.exceptions import RabbitMQConumserMessageError
from src.django_project.apps.video.repository import DjangoORMVideoRepository


class VideoConvertedRabbitMQConsumer(AbstractConsumer):
    def __init__(self, host: str ='localhost', queue: str ="videos.converted"):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {self.host} - {type(self.queue)}')
    
    def on_message(self, message: bytes) -> None:
        print(f"Mensagem recebida {message}")
        self.logger.debug(f"Mensagem recebida {message}")

        try:
            message = json.load(message)

            if message["error"]:
                aggregate_id, _ = message["message"]["resource_id"].split(".")
                raise RabbitMQConumserMessageError(f"Erro ao processar video {aggregate_id}: {message["error"]}")

            aggregate_id, media_type = message["message"]["resource_id"].split(".")
            aggregate_id = UUID(aggregate_id)
            encoded_location = message["video"]["encoded_video_folder"]
            status = MediaStatus(message["status"])

            process_audio_video_media_input = ProcessAudioVideoMediaInput(
                encoded_path=encoded_location,
                video_id=aggregate_id,
                status=status,
                media_type=media_type
            )

            self.logger.debug(f"Chamando caso de uso: {process_audio_video_media_input}")
            use_case = ProcessAudioVideoMedia(video_repository=DjangoORMVideoRepository)
            use_case.execute(request=process_audio_video_media_input)

        except RabbitMQConumserMessageError as err:
            raise RabbitMQConumserMessageError(err)
    
        except Exception as generic_err:
            raise Exception(generic_err)
        
    def start(self):
        self.logger.info(f"Iniciando conexão com RabbitMQ no host {self.host} na fila {self.queue}")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

        # Cria a fila se não existir
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_declare(queue='videos.dlq.rabbitmq', durable=True)
        self.channel.queue_declare(queue='videos.dlq.generic', durable=True)
        
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_message_callback, auto_ack=False, arguments={
            'x-dead-letter-exchange': '',
            'x-dead-letter-routing-key': 'videos.dlq.rabbitmq',
            'x-message-ttl': 60000 
        })

        self.logger.debug("Iniciando consumo da fila!")
        self.channel.start_consuming()
        self.logger.info("Conexão estabelecida e fila sendo consumida!")

    def on_message_callback(self, ch, method, properties, body):
        try:
            self.logger.debug(f"Inicando processamento da mensagem por callback {ch} - {method} - {properties} - {body}")
            self.on_message(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except RabbitMQConumserMessageError as rabbitmq_err:
            self.logger.error(f"Erro ao confirmar mensagem {body} - {rabbitmq_err}")
            self.logger.debug(f"Enviando mensagem novamente para o rabbitmq")
            self.channel.basic_publish(
                exchange='',
                routing_key='videos.dlq.rabbitmq',
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as generic_err:
            self.logger.error(f"Erro genérico ao processar mensagem {body} - {generic_err}")
            self.channel.basic_publish(
                exchange='',
                routing_key='videos.dlq.generic',
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
    def stop(self):
        self.connection.close()
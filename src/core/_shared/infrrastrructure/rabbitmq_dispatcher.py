from dataclasses import asdict
import json

import pika

from src._shared.logger import get_logger
from src.core._shared.events.event import Event
from src.core._shared.infrrastrructure.execptions import RabbitMQConnectionFailed, RabbitMQDisconnectionFailed, RabbitMQSentEventError
from src.core.video.application.use_cases.events.event_dispatcher import EventDispatcherInterface

class RabbitMQDispatcher(EventDispatcherInterface):
    def __init__(self, host='localhost', queue='videos.new'):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None
        self.logger = get_logger(__name__)
        self.logger.debug(f'instância iniciada com {host} - {type(queue)}')
        
    def dispatch(self, event: Event) -> None:
        self.logger.debug(f"Status da conexão para o evento {event}: {self.connection} - fila: {self.queue} - canal: {self.channel}")
        if not self.connection:
            self.logger.info("Conexão não estabelecida, iniciando conexão")
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
            try:
                self.channel.queue_declare(queue=self.queue, durable=True)
            except Exception as err:
                self.logger.error(f"Erro ao estabelecer conexão {err}")
                raise RabbitMQConnectionFailed(err)

        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(event.to_dict()), properties=pika.BasicProperties(delivery_mode=2))
        except Exception as err:
            self.logger.error(f"Erro ao enviar evento para RabbitMQ {err}")
            raise RabbitMQSentEventError(err)
             
        self.logger.info(f"Enviando {event} para a fila {self.queue}")
        print(f"Sent: {event} to queue {self.queue}")

    def close(self):
        self.logger.info("Desconectando RabbitMQ")
        try:
            self.connection.close()
        except Exception as err:
            self.logger.error(f"Erro ao desconectar RabbitMQ {err}")
            raise RabbitMQDisconnectionFailed(err)
            

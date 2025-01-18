from django.core.management.base import BaseCommand

from src.core.video.infra.video_converted_consumer import VideoConvertedRabbitMQConsumer

class Command(BaseCommand):
    help = "Inicia o consumer do rabbimq de videos processados"

    def handle(self, *args, **options):
        consumer =  VideoConvertedRabbitMQConsumer()
        consumer.start()
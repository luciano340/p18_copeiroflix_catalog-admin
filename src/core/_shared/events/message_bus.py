import queue
from typing import Type
from src._shared.logger import get_logger
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.event import Event
from src.core._shared.handler import Handler
from src.core._shared.infrrastrructure.rabbitmq_dispatcher import RabbitMQDispatcher
from src.core.video.application.use_cases.events.handlers import PublishAudioVideoMediaUpdateHandler
from src.core.video.application.use_cases.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent


class MessageBus(AbstractMessageBus):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {
            AudioVideoMediaUpdatedIntegrationEvent: [
                PublishAudioVideoMediaUpdateHandler(
                    event_dispatcher=RabbitMQDispatcher(queue="video.new")
                )
            ]
        }
        self.logger = get_logger(__name__)
    
    def handle(self, events: list[Event]) -> None:
        for event in events:
            handlers = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as err:
                    self.logger.error(f'Error on message bus {err}')
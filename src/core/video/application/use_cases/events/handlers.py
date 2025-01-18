from logging import Handler

from src._shared.logger import get_logger
from src.core.video.application.use_cases.events.event_dispatcher import EventDispatcherInterface
from src.core.video.application.use_cases.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent


class PublishAudioVideoMediaUpdateHandler(Handler):
    def __init__(self, event_dispatcher: EventDispatcherInterface):
        self.event_dispatcher = event_dispatcher
        self.logger = get_logger(__name__)
        
    def handle(self, event: AudioVideoMediaUpdatedIntegrationEvent) -> None:
        self.logger.debug(f'Starting event dispatcher for {event}')
        self.event_dispatcher.dispatch(event)
        self.logger.debug(f'Finished event dispatcher for {event}')
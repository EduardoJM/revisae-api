import logging

from application.interfaces.event_publisher_port import EventPublisherPort
from domain.events.base import DomainEvent

logger = logging.getLogger(__name__)


class LogEventPublisher(EventPublisherPort):
    async def publish(self, event: DomainEvent) -> None:
        logger.info(
            "domain_event",
            extra={
                "event_type": type(event).__name__,
                "occurred_at": event.occurred_at.isoformat(),
                "payload": {
                    k: str(v) for k, v in vars(event).items() if k != "occurred_at"
                },
            },
        )

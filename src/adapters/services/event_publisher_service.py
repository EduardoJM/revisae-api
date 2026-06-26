import logging
import json

import pika
from pika.adapters.blocking_connection import BlockingChannel

from application.interfaces.event_publisher_port import EventPublisherPort
from domain.events.base import DomainEvent

logger = logging.getLogger(__name__)


class LogEventPublisher(EventPublisherPort):
    def __init__(self, channel: BlockingChannel):
        self._channel = channel

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
        self._channel.basic_publish(
            exchange='',
            routing_key=f"domain_event.{type(event).__name__}",
            body=json.dumps({
                "event_type": type(event).__name__,
                "occurred_at": event.occurred_at.isoformat(),
                "payload": {
                    k: str(v) for k, v in vars(event).items() if k != "occurred_at"
                },
            }),
            properties=pika.BasicProperties(
                content_type='text/plain',
                delivery_mode=pika.DeliveryMode.Transient
            )
        )

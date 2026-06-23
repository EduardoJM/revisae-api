from abc import ABC, abstractmethod
from domain.events.base import DomainEvent

class EventPublisherPort(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...

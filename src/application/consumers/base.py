from typing import Type
import asyncio

from dishka import AsyncContainer

from domain.events.base import DomainEvent

class ConsumerBase:
    def __init__(self, container: AsyncContainer, body: dict):
        self.container = container
        self.body = body

    async def execute(self):
        raise NotImplementedError()

class ConsumersRegistry:
    _registry: dict[str, Type[ConsumerBase]] = {}

    @classmethod
    def register(self, name: str, cls):
        print(name)
        if name in self._registry:
            return
        self._registry[name] = cls

    @classmethod
    def get(cls, name: str):
        return cls._registry[name]
    
    @classmethod
    def get_all_consumers(cls):
        return [str(x) for x in cls._registry.keys()]
    
    @classmethod
    async def execute_consumer(cls, name, body, container: AsyncContainer):
        ConsumerClass = cls.get(name)
        instance = ConsumerClass(container, body)
        await instance.execute()

def register_consumer(domain_event_cls: Type[DomainEvent]):
    def _wrapper(cls):
        ConsumersRegistry.register(domain_event_cls.__name__, cls)
        return cls
    return _wrapper

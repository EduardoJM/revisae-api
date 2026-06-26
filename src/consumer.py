import os
import sys
import json
import asyncio
import functools

from dishka import make_async_container

import pika

from infrastructure.config.settings import settings

from infrastructure.providers.providers import (
    DatabaseProvider,
    InfrastructureProvider,
    RepositoryProvider,
    UseCaseProvider,
    RabbitMQProvider,
)
from application.consumers.base import ConsumersRegistry

def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper

def main():
    container = make_async_container(
        RabbitMQProvider(),
        InfrastructureProvider(),
        DatabaseProvider(),
        RepositoryProvider(),
        UseCaseProvider(),
    )

    parameters = pika.URLParameters(settings.broker_url)
    connection = pika.BlockingConnection(parameters)
    channel =  connection.channel()

    queues = ConsumersRegistry.get_all_consumers()
    for queue in queues:
        channel.queue_declare(
            queue=f"domain_event.{queue}",
            durable=True,
            arguments={'x-queue-type': 'classic'}
        )

        @sync
        async def consume(ch, method, properties, body):
            body = json.loads(body)
            await ConsumersRegistry.execute_consumer(queue, body, container)

        channel.basic_consume(
            queue=f"domain_event.{queue}",
            auto_ack=True,
            on_message_callback=consume
        )

    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

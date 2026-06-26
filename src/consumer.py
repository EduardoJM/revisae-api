import os
import sys
import json

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

        def consume(ch, method, properties, body):
            body = json.loads(body)
            ConsumersRegistry.execute_consumer(queue, body, container)

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

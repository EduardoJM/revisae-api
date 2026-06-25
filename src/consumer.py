import os
import sys

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

def callback(ch, method, properties, body):
    print(ch)
    print(method)
    print(properties)
    print(f" [x] Received {body}")

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

    channel.queue_declare(
        queue="domain_event",
        durable=True,
        arguments={'x-queue-type': 'classic'}
    )
    channel.basic_consume(
        queue='domain_event',
        auto_ack=True,
        on_message_callback=callback
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

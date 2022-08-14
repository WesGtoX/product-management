import json
import logging
import os

import pika
from service import APIService

logger = logging.getLogger(__name__)


params = pika.URLParameters(url=os.getenv('BROKER_URL', default=''))
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    logger.info('Receive in main')
    data = json.loads(body)

    service = APIService(data)

    if properties.content_type == 'product_created':
        service.create()

    if properties.content_type == 'product_updated':
        service.update()

    if properties.content_type == 'product_deleted':
        service.delete()


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

logger.info('Started Consuming')

channel.start_consuming()
channel.close()

import json
import logging
import os

import pika

logger = logging.getLogger(__name__)


params = pika.URLParameters(url=os.getenv('BROKER_URL', default=''))
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body).encode(), properties=properties)

    logger.info(method)

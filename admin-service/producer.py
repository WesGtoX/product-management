import json
import logging

import pika
from decouple import config

logger = logging.getLogger(__name__)


params = pika.URLParameters(url=config('BROKER_URL', default=''))
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body).encode(), properties=properties)

    logger.info(method)

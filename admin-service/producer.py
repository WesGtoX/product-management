import json

import pika
from decouple import config

# params = pika.URLParameters(url=settings.BROKER_URL)
params = pika.URLParameters(url='amqps://zripliyj:jfDsB3Ia_uu6QAstDE3L1IMZqYQ4uBjd@jackal.rmq.cloudamqp.com/zripliyj')


params = pika.URLParameters(url=config('BROKER_URL', default=''))
connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body).encode(), properties=properties)

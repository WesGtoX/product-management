import pika
from django.conf import settings

# params = pika.URLParameters(url=settings.BROKER_URL)
params = pika.URLParameters(url='amqps://zripliyj:jfDsB3Ia_uu6QAstDE3L1IMZqYQ4uBjd@jackal.rmq.cloudamqp.com/zripliyj')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method='', body=''):
    # producer = 'admin'
    producer = 'main'
    channel.basic_publish(exchange='', routing_key=producer, body=f'hello world {producer}')

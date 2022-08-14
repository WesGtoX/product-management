import json
import os

import django
import pika
from decouple import config


os.environ['DJANGO_SETTINGS_MODULE'] = 'admin.settings'

django.setup()

from products.models import Product

params = pika.URLParameters(url=config('BROKER_URL', default=''))
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    data = json.loads(body)

    product = Product.objects.get(pk=data.get('pk'))
    product.likes += 1
    product.save()


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
channel.close()

import pika
from django.conf import settings

params = pika.URLParameters(url=settings.BROKER_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Receive in admin')
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

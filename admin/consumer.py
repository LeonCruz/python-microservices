import json
import os

import django
import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="admin")


def callback(channel, method, properties, body):
    print("Received in admin")
    id_ = json.loads(body)

    print(id_)

    product = Product.objects.get(id=id_)
    product.likes += 1
    product.save()

    print("Product likes increased!")


channel.basic_consume(queue="admin", on_message_callback=callback, auto_ack=True)

print("Started consuming")
channel.start_consuming()


channel.close()

import json

import pika

from main import Product, db

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="main")


def callback(channel, method, properties, body):
    print("Received in main")
    data = json.loads(body)
    print(data)

    if properties.content_type == "product_created":
        product = Product(id=data["id"], title=data["title"], image=data["image"])
        print("Product created")
        db.session.add(product)
        db.session.commit()

    elif properties.content_type == "product_updated":
        print("Product updated")
        product = Product.query.get(data["id"])
        product.title = data["title"]
        product.image = data["image"]

        db.session.commit()

    elif properties.content_type == "product_deleted":
        print("Product deleted")
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue="main", on_message_callback=callback, auto_ack=True)

print("Started consuming")
channel.start_consuming()


channel.close()

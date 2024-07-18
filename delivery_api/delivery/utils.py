import pika
from .models import Delivery

def on_message_received(ch, method, properties, body):
    print(f'received: "{body}"')
    try:
        order_details = body['order_data']
        delivery = Delivery.objects.create(
            order_id=order_details['order_id'],
            delivery_provider=order_details['delivery_provider'],
            status=order_details['status'],
            current_location=order_details['address'],
            delivery_method=order_details['delivery_method']
        )
        print(f'Delivery created: {delivery}')
    except Exception as e:
        print(f'Error creating delivery: {str(e)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()
# channel.queue_declare(queue='delivery_queue')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='delivery_queue', on_message_callback=on_message_received)

print('Starting Consuming')

channel.start_consuming()
import pika
import json
from delivery.models import Delivery

def on_message_received(ch, method, properties, body):
    print(f'received: "{body}"')
    try:
        # Decode the byte string
        body_str = body.decode('utf-8')
        
        # Parse the JSON string
        message = json.loads(body_str)
        
        # Extract the relevant data
        order_data = message[0][0]['order_data']
        
        # Create the Delivery object
        delivery = Delivery.objects.create(
            order_id=order_data['id'],
            delivery_provider=order_data['delivery_provider'],
            status=order_data['status'],
            current_location=order_data['address'],
            delivery_method=order_data['delivery_method']
        )
        delivery.save()
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

import pika
import json
from delivery.models import Delivery
from urllib.parse import urlparse
from decouple import config

def on_message_received(ch, method, properties, body):
    print(f'received: "{body}"')
    try:
        # Decode the byte string
        body_str = body.decode('utf-8')
        
        # Parse the JSON string
        message = json.loads(body_str)
        
        # Extract the relevant data
        delivery_data = message[0][0]['order_data']
        
        # Create the Delivery object
        delivery = Delivery.objects.create(
            order_id=delivery_data['id'],
            payment_method=delivery_data['payment_method'],
            status=delivery_data['status'],
            current_location=delivery_data['address'],
            delivery_method=delivery_data['delivery_method']
        )
        delivery.save()
        print(f'Delivery created: {delivery}')
    except Exception as e:
        print(f'Error creating delivery: {str(e)}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

BROKER_URL = config('CLOUDAMQP_URL')
parsed_url = urlparse(BROKER_URL)

connection_parameters = pika.ConnectionParameters(
    host=parsed_url.hostname,
    port=parsed_url.port or 5672,
    virtual_host=parsed_url.path[1:] or '/',
    credentials=pika.PlainCredentials(parsed_url.username, parsed_url.password)
)
try:
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='delivery_queue', on_message_callback=on_message_received)

    print('Starting Consuming')

    channel.start_consuming()
except pika.exceptions.AMQPConnectionError as e:
    print(f'Error connecting to RabbitMQ: {str(e)}')
except Exception as e:
    print(f'An error occurred: {str(e)}')

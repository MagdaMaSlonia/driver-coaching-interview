import json
from time import sleep

from confluent_kafka import Producer
import socket

from data.generate_data import generate_trip_metadata

conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()}

producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))


while True:
    sleep(2)
    # Serve on_delivery callbacks from previous calls to produce()
    producer.poll(0.0)
    try:
        message = generate_trip_metadata()
        key = message['eventType']
        producer.produce(topic='trips', key=key, value=json.dumps(message), callback=acked)
    except KeyboardInterrupt:
        break
    except ValueError:
        print("Invalid input, discarding record...")
        continue

print("\nFlushing records...")
producer.flush()


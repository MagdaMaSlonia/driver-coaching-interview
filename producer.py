import json
import socket

from confluent_kafka import Producer


class DataPublisher:
    def __init__(self):
        conf = {#'bootstrap.servers': 'localhost:9092',
                'bootstrap.servers': 'kafka:9101',
                'client.id': socket.gethostname()}

        self.producer = Producer(conf)

    def acked(self, err, msg):
        if err is not None:
            print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
        else:
            print("Message produced: %s" % (str(msg)))

    def publish_to_topic(self, topic, key, data):

        # Serve on_delivery callbacks from previous calls to produce()
        self.producer.poll(0.0)
        self.producer.produce(topic=topic, key=key, value=json.dumps(data), callback=self.acked)

        print("\nFlushing records...")
        self.producer.flush()

import sys
from time import sleep

from confluent_kafka import Consumer, KafkaError, KafkaException
from trip_message_processor import TripMessageProcessor


###
#todo:
# 2. usuwac po 30 dniach
# 5. testy
# 7. sprawdzic docker
# 9. makefile
# 10. logi


class TripDataConsumer:
    def __init__(self):
        sleep(60)
        self.conf = {#'bootstrap.servers': 'localhost:9092',
            'bootstrap.servers': 'kafka:9101',
                     'group.id': 'foo',
                     'auto.offset.reset': 'smallest'}

        self.consumer = Consumer(self.conf)
        self.topics = ['trips']
        self.trip_message_processor = TripMessageProcessor()

    def process_message(self, message):
        self.trip_message_processor.process(message)

    def consume_data(self):
        try:
            self.consumer.subscribe(self.topics)

            while True:
                messages = self.consumer.poll(timeout=1.0)
                if messages is None:
                    continue

                if messages.error():
                    if messages.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' % (
                        messages.topic(), messages.partition(), messages.offset()))
                    elif messages.error():
                        raise KafkaException(messages.error())
                else:
                    self.process_message(messages)
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()


if __name__ == '__main__':
    TripDataConsumer().consume_data()


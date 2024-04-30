import json

from data_analyzer import DataAnalyzer
from db import TripsDb
from producer import DataPublisher
from trip_data import TripDataRetriever
from validator import Validator


class TripMessageProcessor:
    def __init__(self):
        self.db = TripsDb()
        self.harsh_braking_threshold = 3
        self.data_publisher = DataPublisher()
        self.trip_data_retriever = TripDataRetriever(use_dev_mode=True)
        self.data_analyzer = DataAnalyzer()
        self.validator = Validator()

    def persist_results(self, harsh_braking_count, trip_data, trip_metadata):
        if harsh_braking_count >= self.harsh_braking_threshold:
            self.db.save_trip_analysis(trip_id=trip_data["tripId"],
                                  customer_id=trip_metadata["data"]["entitlement"]["customerId"],
                                  vin=trip_data["vin"],
                                  start_timestamp=trip_data["tripStartTimestamp"],
                                  end_timestamp=trip_data["tripEndTimestamp"],
                                  braking_events_counter=harsh_braking_count)

    def validate_trip_metadata(self, trip_metadata: dict):
        self.validator.validate_trip_metadata(trip_metadata)

    def send_results_to_topic(self, topic: str, key: str, data: dict):
        self.data_publisher.publish_to_topic(topic, key, data)

    def deserialize_data(self, message):
        return json.loads(message.value())

    def process(self, message):
        #deserialize data
        trip_metadata = self.deserialize_data(message)
        #validation
        self.validate_trip_metadata(trip_metadata)
        #get trip data
        trip_data = self.trip_data_retriever.get_trip_data(trip_metadata)
        # remove not compliant messages
        if self.data_analyzer.is_compliant_with_GDPR(trip_metadata):
            return

        if self.data_analyzer.is_speeding_vehicle(trip_metadata):
            self.send_results_to_topic(topic="A", key=trip_data["tripId"], data=trip_metadata)

        harsh_braking_count = self.data_analyzer.count_harsh_braking_events(trip_data)

        #save to db
        self.persist_results(harsh_braking_count=harsh_braking_count, trip_data=trip_data, trip_metadata=trip_metadata)

        self.send_results_to_topic(topic="trip_analysis", key=trip_data["tripId"],
                              data=self.data_analyzer.combine_trip_analysis_data(harsh_braking_count=harsh_braking_count,
                                                                            trip_data=trip_data,
                                                                            trip_metadata=trip_metadata))
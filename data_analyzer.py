from datetime import datetime


class DataAnalyzer:

    def __init__(self):
        self.deceleration_threshold = -18 * 3.6 #(km/h)/s

    def is_compliant_with_GDPR(self, data: dict) -> bool:
        return data["data"]["privacy"]["isPrivacyModeEnabled"]

    def is_speeding_vehicle(self, data: dict) -> bool:
        policies = data["data"]["policy"]["policies"]
        is_speeding = False
        for policy in policies:
            vehicle_signals = policy["vehicleSignals"]
            if "speed" in vehicle_signals:
                is_speeding = True
        return is_speeding

    def calculate_acceleration(self, v0: int, v1: int, time_delta) -> float:
        return (v1 - v0) / time_delta.total_seconds()

    def count_harsh_braking_events(self, trip_data: dict) -> int:
        harsh_braking_events = 0

        events = trip_data["events"]

        for i in range(len(events) - 1):
            event1 = events[i]
            event2 = events[i + 1]

            # skip low gps quality
            if event1["gps_quality"] < 1:
                continue

            v0, v1 = event1["speed"], event2["speed"]
            t0, t1 = event1["recorded_at"], event2["recorded_at"]

            date_format = '%Y-%m-%dT%H:%M:%SZ'
            time_delta = datetime.strptime(t1, date_format) - datetime.strptime(t0, date_format)

            acceleration = self.calculate_acceleration(v0, v1, time_delta)

            if acceleration < self.deceleration_threshold:
                harsh_braking_events += 1

        return harsh_braking_events

    def combine_trip_analysis_data(self, harsh_braking_count, trip_data, trip_metadata) -> dict:
        return {
            "customerId": trip_metadata["data"]["entitlement"]["customerId"],
            "tripId": trip_data["tripId"],
            "vin": trip_data["vin"],
            "tripStartTimestamp": trip_data["tripStartTimestamp"],
            "tripEndTimestamp": trip_data["tripEndTimestamp"],
            "data": {
                "braking_events_counter": harsh_braking_count
            }
        }



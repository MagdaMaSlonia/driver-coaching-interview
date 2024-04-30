import requests as requests

from data.generate_data import generate_trip_data_from_metadata


class TripDataRetriever:
    def __init__(self, use_dev_mode):
        self.use_dev_mode = use_dev_mode

    def get_trip_data(self, metadata: dict) -> dict:
        if self.use_dev_mode:
            return generate_trip_data_from_metadata(metadata)
        else:
            return self.get_trip_data_from_api(metadata)

    def get_trip_data_from_api(self, data: dict):
        url = data["data"]["trip"]["url"]

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

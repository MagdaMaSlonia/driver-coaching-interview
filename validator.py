from pydantic import ValidationError
from models.trip_meta import Payload


class Validator:

    def validate_trip_metadata(self, json_data):
        try:
            Payload.model_validate(json_data)
        except ValidationError as e:
            raise e


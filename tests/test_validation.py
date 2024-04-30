import json

import pytest
from pydantic import ValidationError

from validator import Validator


def test_validation_is_working():
    with open('../data/trip_metadata.json') as f:
        data = json.load(f)
        validator = Validator()
        validator.validate_trip_metadata(data)


def test_validation_failes():
    with pytest.raises(ValidationError):
        validator = Validator()
        validator.validate_trip_metadata({"aaa":"bbb"})

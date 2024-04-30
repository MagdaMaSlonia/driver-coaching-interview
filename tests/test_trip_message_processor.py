import json
from unittest.mock import MagicMock

import pytest
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker

from models.trip_analysis import TripAnalysisDB, Base
from trip_message_processor import TripMessageProcessor


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestSession()


def test_message_process(session):
    #given
    processor = TripMessageProcessor()
    with open('../data/trip_metadata.json') as f:
        data = json.load(f)
    processor.deserialize_data = MagicMock(return_value=data)
    processor.data_publisher = MagicMock()
    message = "some_data"
    processor.db.session = session
    with open('../data/trip_analysis.json') as f:
        trip_analysis = json.load(f)
    #when
    processor.process(message)

    #then
    created_object = processor.db.session.query(TripAnalysisDB).one_or_none()
    assert created_object.vin == "VIN100362"
    braking_events_counter = created_object.brakingEventsCounter
    trip_analysis["data"]["braking_events_counter"] = braking_events_counter
    processor.data_publisher.publish_to_topic.assert_called_with("trip_analysis", "7cc5df0d-4b72-4b2b-b1ed-20835a1b7f4b", trip_analysis)
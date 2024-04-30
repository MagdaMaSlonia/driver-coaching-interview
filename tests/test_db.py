# todo: 1. test, ze dobre dane sie zapisza i odczyta sie cos z bazy
#        2. test ze zle dane sie nie zapisza
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import TripsDb
from models.trip_analysis import Base, TripAnalysisDB


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return TestSession()


def test_adding_to_db_success(session):
    trip_id = "79b2c991-36aa-4fac-8756-a181a5fa282d"
    customer_id = "ef28f877-206a-44c3-8af9-713f54657482"
    vin = "VIN100362"
    start_timestamp = "2024-03-19 16:25:24.262139"
    end_timestamp = "2024-03-19 16:30:24.262139"
    braking_events_counter = 6
    db = TripsDb()
    db.session = session
    trip_analysis = db.save_trip_analysis(trip_id=trip_id, customer_id=customer_id, vin=vin,
                                          start_timestamp=start_timestamp, end_timestamp=end_timestamp,
                                          braking_events_counter=braking_events_counter)
    assert trip_analysis.tripId == trip_id
    assert trip_analysis.brakingEventsCounter == braking_events_counter
    created_object = db.session.query(TripAnalysisDB).one_or_none()
    assert created_object.vin == "VIN100362"



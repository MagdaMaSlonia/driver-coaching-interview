from datetime import datetime
from importlib import resources

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.trip_analysis import TripAnalysisDB, Base


class TripsDb:
    def __init__(self):
        self.db = "trips.db"
        self.number_of_days_to_outdate = 30

        self.init_db()

    def init_db(self):
        with resources.path(
                "data", self.db
        ) as sqlite_filepath:
            engine = create_engine(f"sqlite:///{sqlite_filepath}")
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        #session.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.session = Session()


    def save_trip_analysis(self, trip_id, customer_id, vin, start_timestamp, end_timestamp, braking_events_counter):
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        trip_analysis = TripAnalysisDB(tripId=trip_id, customerId=customer_id, vin=vin,
                                       tripStartTimestamp=datetime.strptime(start_timestamp, date_format),
                                       tripEndTimestamp=datetime.strptime(end_timestamp, date_format),
                                       brakingEventsCounter=braking_events_counter,
                                       timestamp=datetime.now())
        self.session.add(trip_analysis)

        self.session.commit()

        return trip_analysis

    def delete_outdated_entries(self):
        pass

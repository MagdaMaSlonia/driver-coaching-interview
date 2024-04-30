import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Table, UUID, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TripAnalysisDB(Base):
    __tablename__ = "trip_analysis"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    tripId = Column(String)
    customerId = Column(String)
    vin = Column(String)
    tripStartTimestamp = Column(DateTime)
    tripEndTimestamp = Column(DateTime)
    brakingEventsCounter = Column(Integer)
    timestamp = Column(DateTime)


class TripAnalysis(BaseModel):
    id: uuid.UUID
    tripId: uuid.UUID
    customerId: uuid.UUID
    vin: str
    tripStartTimestamp: datetime
    tripEndTimestamp: datetime
    brakingEventsCounter: int
    timestamp: datetime

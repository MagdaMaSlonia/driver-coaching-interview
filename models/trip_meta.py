# generated by datamodel-codegen:
#   filename:  trip.metadata.yaml
#   timestamp: 2024-04-28T13:22:43+00:00

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import AnyUrl, BaseModel, confloat


class Entitlement(BaseModel):
    customerId: UUID
    locale: str


class Privacy(BaseModel):
    isPrivacyModeEnabled: bool


class Vehicle(BaseModel):
    vin: str


class Policy1(BaseModel):
    id: str
    vehicleSignals: List[str]
    notBefore: datetime
    expiresAt: datetime


class Policy(BaseModel):
    inUseAt: datetime
    retrievedAt: datetime
    vehicle: Vehicle
    policies: List[Policy1]


class Trip(BaseModel):
    vin: str
    tripId: str
    tripDistance: float
    tripStartTimestamp: datetime
    tripStartLat: float
    tripStartLon: float
    tripEndTimestamp: datetime
    tripEndLat: float
    tripEndLon: float
    fuelLevel: confloat(ge=0.0, le=100.0)
    url: AnyUrl


class Data(BaseModel):
    entitlement: Entitlement
    privacy: Privacy
    policy: Policy
    trip: Trip


class Payload(BaseModel):
    id: UUID
    version: str
    eventTime: datetime
    eventType: str
    data: Data

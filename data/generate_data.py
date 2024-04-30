import json
import random
import uuid
from datetime import datetime, timedelta


# Based on the provided trip metadata, generating detailed trip data with event points


def generate_trip_metadata():
    trip_id = str(uuid.uuid4())
    vin = "VIN" + str(random.randint(100000, 999999))
    trip_distance = round(random.uniform(5.0, 50.0), 2)  # in kilometers
    fuel_level_start = random.randint(50, 100)
    fuel_level_end = fuel_level_start - random.randint(1, 10)  # assume some fuel consumption
    start_lat = round(random.uniform(50.0, 52.0), 6)
    start_lon = round(random.uniform(-1.0, 1.0), 6)
    end_lat = start_lat + round(random.uniform(-0.01, 0.01), 6)
    end_lon = start_lon + round(random.uniform(-0.01, 0.01), 6)
    trip_start_time = datetime.now() - timedelta(days=random.randint(1, 30))
    trip_end_time = trip_start_time + timedelta(minutes=random.randint(5, 10))

    trip = {
        "id": str(uuid.uuid4()),
        "version": "1.0.0",
        "eventTime": str(datetime.now()),
        "eventType": "tripData",
        "data": {
            "entitlement": {
                "customerId": str(uuid.uuid4()),
                "locale": "en-US"
            },
            "privacy": {
                "isPrivacyModeEnabled": random.choice([True, False])
            },
            "policy": {
                "inUseAt": str(trip_start_time),
                "retrievedAt": str(trip_end_time),
                "vehicle": {
                    "vin": vin
                },
                "policies": [
                    {
                        "id": str(uuid.uuid4()),
                        "vehicleSignals": ["speed", "location"],
                        "notBefore": str(trip_start_time),
                        "expiresAt": str(trip_end_time)
                    }
                ]
            },
            "trip": {
                "vin": vin,
                "tripId": trip_id,
                "tripDistance": trip_distance,
                "tripStartTimestamp": str(trip_start_time),
                "tripStartLat": start_lat,
                "tripStartLon": start_lon,
                "tripEndTimestamp": str(trip_end_time),
                "tripEndLat": end_lat,
                "tripEndLon": end_lon,
                "fuelLevel": fuel_level_end,
                "url": f"https://trip-service.toyotaconnectedeurope.io/trip?vin={vin}&tripStartTimestamp={trip_start_time.isoformat() + 'Z'}"
            }
        }
    }

    return trip


# Simulating the trip data returned by hitting the endpoint
def generate_trip_data_from_metadata(trip_metadata):
    start_datetime = trip_metadata["data"]["trip"]["tripStartTimestamp"]
    end_datetime = trip_metadata["data"]["trip"]["tripEndTimestamp"]
    date_format = '%Y-%m-%d %H:%M:%S.%f'
    print(f'start_datetime: {start_datetime}')

    duration_in_seconds = int((datetime.strptime(end_datetime, date_format) - datetime.strptime(start_datetime, date_format)).total_seconds())

    # Generating GPS events at one-minute intervals
    events = []
    for seconds in range(0, duration_in_seconds, 1):
        event_time = datetime.strptime(start_datetime, date_format) + timedelta(seconds=seconds)
        events.append({
            "gps_quality": random.choices([0, 1], weights=[20, 80], k=1)[0],
            "lat": round(51.119457 + ((seconds / 60) * 0.0001), 6),  # Simulating slight movement
            "lng": round(0.38939 + ((seconds / 60) * 0.0001), 6),
            "recorded_at": event_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "speed": random.randint(20, 100)
        })

    # Constructing the full trip data payload
    trip_data = {
        "tripId": trip_metadata["data"]["trip"]["tripId"],
        "vin": trip_metadata["data"]["trip"]["vin"],
        "tripStartTimestamp": trip_metadata["data"]["trip"]["tripStartTimestamp"],
        "tripEndTimestamp": trip_metadata["data"]["trip"]["tripEndTimestamp"],
        "events": events
    }

    return trip_data


def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat() + 'Z'
    raise TypeError("Unknown type")


if __name__ == '__main__':
    trip_metadata = generate_trip_metadata()
    # Generate the detailed trip data
    full_trip_data = generate_trip_data_from_metadata(trip_metadata)
    print(f"{'#' * 115}")
    print(f"{'#' * 50} Trip metadata {'#' * 50}")
    print(f"{'#' * 115}")
    print(json.dumps(trip_metadata, indent=4, default=datetime_handler))
    print(f"{'#' * 111}")
    print(f"{'#' * 50} Trip data {'#' * 50}")
    print(f"{'#' * 111}")
    print(json.dumps(full_trip_data, indent=4, default=datetime_handler))

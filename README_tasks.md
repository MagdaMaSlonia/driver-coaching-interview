# Driver Behavior coding challenge

## Problem Statement: Driver Behavior Analysis

### Background:

You are a Python Software Engineer at an automotive technology company that
specializes in developing innovative solutions for connected vehicles.
Your latest project involves creating a system that processes trip data from
vehicles to analyze driving behavior. Based on this analysis,
the system will provide personalized driving advice to vehicle owners
and share relevant data with insurance companies to potentially
adjust insurance premiums or offer rewards for safe driving.

### analiza jazd samochodow
### na tej podstawie daje rekomendacje kierowcom oraz firmom ubezpieczeniowym

### Data:

The system will receive trip data in real-time through a Kafka topic.
For which the asyncapi definition can be found here: [input trip metadata asyncapi.yml](specs/trip.metadata.yaml)
and [trip metadata example](data/trip_metadata.json).
Each message represents a trip made by a vehicle, containing trip metadata details such as
vehicle ID (VIN), trip start and end timestamps, trip start and end GPS route data, fuelLevel etc.

### wiadomosci w realtime przez kafkę, message wygląda jak ten wyzej

To get the full trip you can query an endpoint owned and maintained by another Team. The definition can be
found here: [get full trip from endpoint openapi.yml](specs/trip.api.yaml) and [trip data example](data/trip_data.json)
Using the URL found in the trip metadata, you should be able to query a trip. For the sake of this exercise, please mock
the endpoint in your test to be returning the trip data.

### jest enpoint ktory zwraca nam calą jazdę, jest jego definicja, można pobra sobie trip
### zamokowac dane, tak ze zwraca zawsze ten dane
  
### Objective:

#### 1. Driver Behavior Service:

Develop a Python service to consume trip data from the Kafka topic in real-time.
Analyze the trip data to assess driving behavior.


### zrob serwis, ktory pobierze dane z kafki w real-time, zaanalizuj je
### zanalizuj driving behavior

- Implement the service such that it can be executed locally on your machine.
  Please ensure the service is also packaged in a way which allows it to be deployed and
  scaled easily. Detailed instructions on how to build and run the service should be included in
  the README.md.

### serwis ma byc lokalny ale trzeba go odokerowac
### dodaj readme
### dodaj kontener

- Input data validation is crucial. Ensure that the data received through Kafka is validated against
  expected formats. Discard any trips marked as private immediately to comply with
  GDPR, and check for GPS quality - must be good (=1)

### zwaliduj dane
### usun dane prywatne
### GPS quality musi byc good


- Define the output data format clearly. Ensure that results from the trip data analysis are pushed to the specified
  Kafka topics in a structured format that can be easily integrated with downstream systems. Include examples of the
  output data format in your documentation.

### jakas analiza i ładne opakowanie danych
### daj przyklady outputow
### wrzuc dane na kafke


- Include a testing suite that validates the functionality and robustness of your service. Use mocking frameworks to
  simulate the external Trip API responses. Consider using testcontainers if you choose to implement integration tests
  that involve Kafka or other external dependencies. Tests should cover data validation, correct routing of trip data,
  and proper handling of Kafka messages.

### hardcorowe testy


- (Bonus) Implement comprehensive error handling to manage potential data quality issues and external integration
  failures. Provide detailed logging of both normal operation and error conditions to aid in troubleshooting and
  monitoring of the system’s performance.

### error handling

#### 2. Trip Data Routing and Computing:

##### 2.1 Model A: Identifying and Counting Harsh Braking Events from Trip Data

Trip should be routed to the Harsh Braking Counter Model if and only if we have a `vehicleSignal`= `speed` policy
attached to that vehicle and should go to topic A


### jesli vehicleSignal oznacza, ze ktos speedowal, to wysylamy NUMER POLICY na topic A 

Given a sequence of events for a trip, where each event contains a speed in km/h (kilometers per hour) and a timestamp (
recorded_at in ISO 8601 format),
identify "harsh braking" events and return the count of harsh braking events per trip. A harsh braking event is defined
as a change in speed (deceleration) greater than a
specified threshold (in km/h per second) between two consecutive events.


### wylicz harsh braking events pomiedzy eventami

Assume the speed is measured exactly at the timestamp, and use the difference between consecutive timestamps and speeds
to calculate acceleration (or deceleration). Consider the deceleration threshold to be 2 times the gravity, approximated
at -18 m/s² (meters per second squared)
for this exercise, which needs to be converted appropriately to match the speed units in the data.
Use the conversion factor of 3.6 to convert m/s² to km/h per second

### predkosc liczona jest na timestamp

Acceleration is calculated as: <p>a = (V<sub>1</sub> - V<sub>0</sub>) / (t<sub>1</sub> - t<sub>0</sub>)</p>

- `a`: Acceleration
- `V1`: Final velocity
- `V0`: Initial velocity
- `t1`: time at final state
- `t0`: Time at initial state

### tu wzor na przyspieszenie

Implement functionality to store trips with more than 3 harsh braking events in a database. Each entry should include
the vehicle ID, trip ID, count of harsh braking events, and the timestamp of storage. Entries should be retained for 30
days before being automatically deleted.


### przechowaj jazdy z eventami dluzszymi niz 30 dni, automatycznie maja sie czyscic

##### (bonus) 2.2 Model X:

Trip should be routed to Model X if and only if `policyX` is found in the `vehicleSignals` and should go to
topic `topicX`

Other trips should be discarded and logged as warning.

Please take into consideration that in the future, some other Data Science Model and output routing will be added.

#### 3. Documentation and Testing:

Provide comprehensive documentation on system setup, running the service, and how to produce sample trip data for
testing. (README.md)
Include a testing suite to validate the functionality of your service. For the sake of this exercise,
no extensive test coverage is expected but at least one test per kind of test you'd apply here.


### todo:
jak mokowac kafke?
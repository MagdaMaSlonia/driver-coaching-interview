# How to start application

## 1. setting Kafka

First make sure that appropriate topics are created:
 You should have created 3 topics: 
### trips, A, trip_analysis
To get list of topics on confluent Kafka use command:
```
confluent local kafka  topic list
```
Add topics if needed:
```
confluent local kafka  topic create trips
```
## 2. To launch consumer locally use command:
```
python consumer.py
```
## 3. If you are testing program locally and you need real time data to produce data for Kafka, use:
```
python real_time_data_producer.py
```

3. You can use Dockerfile
4. export DOCKER_DEFAULT_PLATFORM=linux/arm64

### App structure:
    - /data: contains examples of data and db file
    - /models: validation models
    - /specs: openapi specification
    - /tests: tests
    - consumer.py - entry point to the application, code responsible for receiving messages
    - data_analyzer.py - code responsible for analyzing data and performing calculations
    - db.py - database
    - Dockerfile
    - producer.py - publish messages to Kafka topics
    - real_time_data_producer.py - script for creating real time data for kafka
    - requirements.txt
    - trip_data.py - enpoint for trips api, currently mocked
    - trip_message_processor - process messages
    - validator.py - code responsible for validation

    
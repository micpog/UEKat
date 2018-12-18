# Real-time meetup rsvp analytics

1. In order to integrate with Spark Streaming using python, download Kafka 2.11-0.9.0.1. 
2. Download Spark version 2.2.0
3. Start Zookeeper server: `.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties`
4. Start Kafka server: `.\bin\windows\kafka-server-start.bat .\config\server.properties`
5. Run Producer script: `python MeetupRsvpProducer.py`
6. Run Consumer script:`python MeetupRsvpConsumer.py`
7. Submit Spark job: `bin\spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.2 spark_meetup.py localhost:2181 meetup`


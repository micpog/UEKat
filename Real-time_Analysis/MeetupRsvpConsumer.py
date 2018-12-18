from kafka import KafkaConsumer

consumer = KafkaConsumer('meetup')

for message in consumer:
    print(message)
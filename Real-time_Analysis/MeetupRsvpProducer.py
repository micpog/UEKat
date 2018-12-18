from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers='localhost:9092')
r = requests.get("https://stream.meetup.com/2/rsvps",stream=True)

for line in r.iter_lines():
    producer.send('meetup', line)
    print(type(line))

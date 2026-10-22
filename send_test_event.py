from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

event = {
    "ip": "1.2.3.4",
    "host": "example.com",
    "event_time": "2023-09-01T12:00:00.000Z"
}

producer.send('web-events', event)
producer.flush()
print("✅ Event sent!")

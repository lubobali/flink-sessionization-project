from kafka import KafkaProducer
import json
import time

# Connect to Kafka inside Docker
bootstrap_servers = "kafka:9092"
topic = "web-events"

print("🔌 Connecting to Kafka at", bootstrap_servers + "...")

try:
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    print(f"✅ Connected. Sending event to topic '{topic}'...")

    event = {
        "url": "/home",
        "referrer": "https://google.com",
        "user_agent": "Mozilla/5.0",
        "host": "example.com",
        "ip": "1.2.3.4",
        "headers": "{}",
        "event_time": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    }

    producer.send(topic, value=event)
    producer.flush()
    print("✅ Event sent.")
except Exception as e:
    print("❌ Failed to send event.")
    print(e)


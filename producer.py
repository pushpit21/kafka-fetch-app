import json, uuid, time
from confluent_kafka import Producer
from client import get_producer

def produce_message(producer, topic, message):
    producer.produce(topic, json.dumps(message).encode('utf-8'))
    producer.flush()

if __name__ == "__main__":
    producer = get_producer()
    topic = 'user-login'
    
    num_messages = 10
    for i in range(num_messages):
        message = {
            "user_id": str(uuid.uuid4()),
            "app_version": "2.3.0",
            "device_type": "android",
            "ip": "199.172.111.135",
            "locale": "RU",
            "device_id": str(uuid.uuid4()),
            "timestamp": str(int(time.time())),
            "message_count": i
        }
        produce_message(producer, topic, message)
        print(f"Produced message #{i}: {message}")

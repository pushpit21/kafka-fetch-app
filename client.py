from confluent_kafka import Consumer, Producer, KafkaError
from confluent_kafka.admin import AdminClient
import logging

KAFKA_BROKER = 'localhost:29092'

def get_producer():
    producer_conf = {
        'bootstrap.servers': KAFKA_BROKER
    }
    return Producer(producer_conf)

def get_consumer(group_id, topic):
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'  # Start reading from the earliest message
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    return consumer

def get_admin_client():
    admin_client_conf = {
        'bootstrap.servers': KAFKA_BROKER
    }
    return AdminClient(admin_client_conf)

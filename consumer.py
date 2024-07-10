import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from client import get_consumer, get_producer
from producer import produce_message
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def consume_messages(consumer):
    """Consume messages from the topic."""
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.info(f"Reached end of partition at offset {msg.offset()}")
            elif msg.error():
                logging.error(msg.error())
                raise KafkaException(msg.error())
        else:
            message = json.loads(msg.value().decode('utf-8'))
            logging.info(f"Consumed message: {message}")
            yield message

def process_message(message):
    """Process the message and return the processed message."""
    # Perform any processing or analysis here. For now, we'll just return the same message.
    return message

def main():
    input_topic = 'user-login'
    output_topic = 'processed-user-login'
    consumer = get_consumer(group_id="consumer-group-1", topic=input_topic)
    producer = get_producer()
    
    for message in consume_messages(consumer):
        processed_message = process_message(message)
        produce_message(producer, output_topic, processed_message)
        logging.info(f"Processed and produced message: {processed_message}")

    # Close the consumer and producer when done
    consumer.close()
    producer.flush()

if __name__ == "__main__":
    main()

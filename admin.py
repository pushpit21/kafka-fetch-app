from client import get_admin_client
from confluent_kafka.admin import NewTopic, KafkaException
from confluent_kafka import KafkaError

def create_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = get_admin_client()
    topic_list = [NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]
    try:
        future = admin_client.create_topics(new_topics=topic_list, validate_only=False)
        for topic, f in future.items():
            f.result()  # The result itself is None
            print(f"Topic {topic_name} created with {num_partitions} partitions")
    except KafkaException as e:
        if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
            print(f"Topic {topic_name} already exists.")
        else:
            print(f"Failed to create topic {topic_name}: {e}")

def list_topics():
    admin_client = get_admin_client()
    metadata = admin_client.list_topics(timeout=10)
    print("Kafka Cluster Metadata:")
    for topic in metadata.topics.values():
        print(f"Topic: {topic.topic}")
        for partition in topic.partitions.values():
            print(f"  Partition: {partition.id}, Leader: {partition.leader}, Replicas: {partition.replicas}, ISR: {partition.isrs}")

if __name__ == "__main__":
    create_topic('user-login', num_partitions=1)
    create_topic('processed-user-login', num_partitions=1)
    list_topics()  # List topics to verify the current state

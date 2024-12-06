from confluent_kafka import Consumer, KafkaException
from minio import Minio
import json
import os
from datetime import datetime

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',  
    'group.id': 'samsung-stock-consumer',   
    'auto.offset.reset': 'earliest'         
}

# Initialize Kafka Consumer
consumer = Consumer(consumer_config)

# Kafka Topic
topic = "samsung-stock-data"

# Minio Client Configuration
minio_client = Minio(
    'localhost:9000',  
    access_key='minio', 
    secret_key='minio123',  
    secure=False  
)

# Create a Minio Bucket (if it doesn't exist)
bucket_name = "samsung-stock-bucket"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

# Process and store the message in Minio
def store_in_minio(message):
    # Create a unique file name (using date or message key)
    file_name = f"samsung-stock-{message['date']}.json"

    # Save the message to a JSON file
    with open(file_name, 'w') as f:
        json.dump(message, f)

    # Upload to Minio
    try:
        minio_client.fput_object(bucket_name, file_name, file_name)
        print(f"Data uploaded to Minio: {file_name}")
    except Exception as e:
        print(f"Error uploading to Minio: {e}")
    
    # Clean up the local file
    os.remove(file_name)

def consume_messages():
    # Subscribe to the Kafka topic
    consumer.subscribe([topic])

    try:
        # Start consuming messages
        while True:
            messages = consumer.consume(num_messages=10, timeout=1.0)  # Consume up to 10 messages at a time
            if not messages:  # No messages available within the timeout
                continue

            for msg in messages:
                if msg.error():  # Error while fetching the message
                    raise KafkaException(msg.error())
                else:
                    # Deserialize the message
                    message = json.loads(msg.value().decode('utf-8'))
                    print(f"Message consumed: {message}")
                    store_in_minio(message)

    except KeyboardInterrupt:
        print("Consuming stopped by user.")
    finally:
        # Close the consumer when done
        consumer.close()

# Start consuming messages and storing them in Minio
consume_messages()

import json
import time
from kafka import KafkaConsumer, KafkaProducer
import threading

# Kafka configuration
bootstrap_servers = 'localhost:9092'
song_topic = 'sendsong'
recommendation_topic = 'recommendedsongs'

# Setup Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[bootstrap_servers],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def send_song_name(song_name):
    """Send the song name to the Kafka topic."""
    producer.send(song_topic, {'song_name': song_name})
    producer.flush()
    print(f"Sent '{song_name}' to topic '{song_topic}' for recommendation processing.")

# Setup Kafka consumer
consumer = KafkaConsumer(
    recommendation_topic,
    bootstrap_servers=[bootstrap_servers],
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

def listen_for_recommendations():
    """Listen for recommendations from the Kafka topic and print them."""
    for message in consumer:
        recommendations = message.value['recommendations']
        print("\nReceived Recommendations:")
        for rec in recommendations:
            print(f"Song: {rec['song']}, Similarity: {rec['similarity']:.2f}")
        print("\nEnter another song name for recommendations:")

def main():
    threading.Thread(target=listen_for_recommendations, daemon=True).start()
    while True:
        song_name = input("Enter a song name to get recommendations (or type 'exit' to quit): ")
        if song_name.lower() == 'exit':
            break
        send_song_name(song_name)
        time.sleep(1)  # Sleep briefly to allow for processing

if __name__ == "__main__":
    main()


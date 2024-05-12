from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)



def send_recommendations(recommendations):
    """Sends the formatted recommendations to the Kafka topic 'recommendedsongs'."""
    message = {'recommendations': recommendations}
    producer.send('recommendedsongs', message)
    producer.flush()
    print(f"Sent recommendations to 'recommendedsongs' topic: {message}")

if __name__ == "__main__":
    # Example call (for testing purposes)
    test_recommendations = [{'song': 'Song A', 'similarity': 0.95}, {'song': 'Song B', 'similarity': 0.90}]
    send_recommendations(recommendations)


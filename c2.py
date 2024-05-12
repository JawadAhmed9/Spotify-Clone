from kafka import KafkaConsumer
import json

def listen_for_recommendations():
    consumer = KafkaConsumer(
        'recommendedsongs',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        recommendations = message.value['recommendations']
        print("\nReceived Recommendations:")
        for rec in recommendations:
            print(f"Song: {rec['song']}, Similarity: {rec['similarity']:.2f}")
        print("\nWaiting for new song input for recommendations:")

if __name__ == '__main__':
    listen_for_recommendations()


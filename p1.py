from kafka import KafkaProducer
import json

def send_song_name():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

    while True:
        song_name = input("Enter a song name to get recommendations (or type 'exit' to quit): ")
        if song_name.lower() == 'exit':
            break
        producer.send('sendsong', {'song_name': song_name})
        producer.flush()
        print(f"Sent '{song_name}' to topic 'sendsong' for recommendation processing.")

if __name__ == "__main__":
    send_song_name()


from kafka import KafkaConsumer
import json
from spark import main

consumer = KafkaConsumer(
    'sendsong',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    song_name = message.value['song_name']
    print(f"Received request for recommendations for: {song_name}")
    recommendations = main(song_names)  # Call the Spark function
    print(f"Recommendations for {song_name}: {recommendations}")

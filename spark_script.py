import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.ml.linalg import Vectors, VectorUDT
import numpy as np
from annoy import AnnoyIndex
from p2 import send_recommendations  # Importing the sending function from producer2

def setup_spark_session():
    spark = SparkSession.builder \
    .appName("MusicRecommendationSystem") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/audio_features.features") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()
    return spark

def fetch_data(spark):
    df = spark.read.format("mongo").load()
    to_vector_udf = udf(lambda x: Vectors.dense(x), VectorUDT())
    df = df.withColumn("features_vec", to_vector_udf("features"))
    return df.select("features_vec", "song_name").rdd.map(lambda x: (x[0].toArray(), x[1])).collect()

def build_index(feature_data):
    dimensions = len(feature_data[0])
    ann_index = AnnoyIndex(dimensions, 'angular')
    for i, vector in enumerate(feature_data):
        ann_index.add_item(i, vector)
    ann_index.build(10)
    return ann_index

def find_similar_items(ann_index, song_index, feature_data, num_results=10):
    similar_items = ann_index.get_nns_by_item(song_index, num_results + 1, include_distances=False)[1:]
    return [(song_names[idx], cosine_similarity(feature_data[song_index], feature_data[idx])) for idx in similar_items]

def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def main(song_name):
    spark = setup_spark_session()
    features_and_names = fetch_data(spark)
    feature_data = [fn[0] for fn in features_and_names]
    song_names = [fn[1] for fn in features_and_names]
    ann_index = build_index(feature_data)
    recommendations = find_similar_items(ann_index, song_names.index(song_name), feature_data) if song_name in song_names else []
    send_recommendations(recommendations)  # Send recommendations to Kafka
    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: spark-submit spark.py <song_name>")
        sys.exit(1)
    song_name = sys.argv[1]
    main(song_name)


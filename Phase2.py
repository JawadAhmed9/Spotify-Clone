import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
from pyspark.ml.linalg import Vectors, VectorUDT
import numpy as np
from annoy import AnnoyIndex


def setup_spark_session():
    return SparkSession.builder \
        .appName("MusicRecommendationSystem") \
        .config("spark.mongodb.input.uri", "mongodb://localhost:27017/audio_features.features") \
        .getOrCreate()


def find_similar_items(item_index, ann_index, num_results=10):
    similar_items = ann_index.get_nns_by_item(
        item_index, num_results + 1, include_distances=False)
    return similar_items[1:]


def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))


if __name__ == "_main_":
    # Check for song name argument
    if len(sys.argv) != 2:
        print("Usage: spark-submit this_script.py <song_name>")
        sys.exit(1)

    song_name = sys.argv[1]
    spark = setup_spark_session()

    # Load data from MongoDB
    df = spark.read.format("mongo").load()

    # Convert array of features to dense vector and include song names
    to_vector_udf = udf(lambda x: Vectors.dense(x), VectorUDT())
    df = df.withColumn("features_vec", to_vector_udf("features"))

    # Collect feature data and song names
    features_and_names = df.select("features_vec", "song_name").rdd.map(
        lambda x: (x[0].toArray(), x[1])).collect()
    feature_data = [fn[0] for fn in features_and_names]  # feature vectors
    song_names = [fn[1] for fn in features_and_names]  # song names

    # Build ANN index
    ann_index = AnnoyIndex(len(feature_data[0]), 'angular')
    for i, vector in enumerate(feature_data):
        ann_index.add_item(i, vector)
    ann_index.build(10)

    if song_name in song_names:
        song_index = song_names.index(song_name)
        similar_items_indices = find_similar_items(song_index, ann_index)
        similarities = [cosine_similarity(
            feature_data[song_index], feature_data[idx]) for idx in similar_items_indices]
        sorted_similarities = sorted(
            zip(similar_items_indices, similarities), key=lambda x: x[1], reverse=True)

        # Display the top 10 best matches with song names
        print(f"Finding songs similar to '{song_name}':")
        print("Top 10 Matches:")
        for index, sim in sorted_similarities:
            print(f"Song: {song_names[index]}, Similarity: {sim:.2f}")
    else:
        print(f"No recommendations found for song: {song_name}")

    spark.stop()

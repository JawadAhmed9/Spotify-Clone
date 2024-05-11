from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import FloatType, StringType, ArrayType
from pyspark.ml.linalg import Vectors, VectorUDT
import numpy as np
from annoy import AnnoyIndex

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("MusicRecommendationSystem") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/audio_features.features") \
    .getOrCreate()

# Load data from MongoDB
df = spark.read.format("mongo").load()

# Convert array of features to dense vector and include song names
to_vector_udf = udf(lambda x: Vectors.dense(x), VectorUDT())
df = df.withColumn("features_vec", to_vector_udf("features"))

# Collect feature data and song names from Spark to Python list
features_and_names = df.select("features_vec", "song_name").rdd.map(lambda x: (x[0].toArray(), x[1])).collect()
feature_data = [fn[0] for fn in features_and_names]  # feature vectors
song_names = [fn[1] for fn in features_and_names]    # song names

dimensions = len(feature_data[0])

# Build ANN index
ann_index = AnnoyIndex(dimensions, 'angular')  # Using 'angular' for cosine similarity
for i, vector in enumerate(feature_data):
    ann_index.add_item(i, vector)
ann_index.build(10)  # 10 trees

# Function to find similar items
def find_similar_items(item_index, num_results=10):
    similar_items = ann_index.get_nns_by_item(item_index, num_results + 1, include_distances=False)  # Fetch one extra to exclude the input itself
    return similar_items[1:]  # Exclude the first one which is the input itself

# Use the first audio as input and find top 10 similar songs
input_index = 0  # Index for the first audio
input_song_name = song_names[input_index]  # Get the name of the song used as the input for recommendations
similar_items_indices = find_similar_items(input_index, 10)  # Fetch top 10 similar

# Calculate cosine similarity
def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

# Retrieve vectors for the similar items
similar_vectors = [feature_data[idx] for idx in similar_items_indices]

# Compute cosine similarity for the 10 similar items
base_vector = feature_data[input_index]
similarities = [cosine_similarity(base_vector, vec) for vec in similar_vectors]

# Sort by similarity
sorted_similarities = sorted(zip(similar_items_indices, similarities), key=lambda x: x[1], reverse=True)

# Display the top 10 best matches with song names
print(f"Finding songs similar to '{input_song_name}':")

print("Top 10 Matches:")
for index, sim in sorted_similarities:
    print(f"Song: {song_names[index]}, Similarity: {sim:.2f}")

spark.stop()


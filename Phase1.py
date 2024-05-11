import os
import librosa
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pymongo import MongoClient
import logging
from concurrent.futures import ProcessPoolExecutor

# Setup logging
logging.basicConfig(level=logging.INFO)

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['audio_features']
collection = db['features']

audio_dir = r'C:\Users\PC\Documents\Symmester 4\Big Data\Assignment 4\data\BDS A\000'


def extract_features(file_path):
    try:
        audio, sample_rate = librosa.load(file_path, sr=None)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        spectral_centroids = librosa.feature.spectral_centroid(
            y=audio, sr=sample_rate)
        zero_crossing = librosa.feature.zero_crossing_rate(y=audio)
        features = np.concatenate((np.mean(mfccs, axis=1),
                                   np.mean(spectral_centroids, axis=1),
                                   np.mean(zero_crossing, axis=1)))
        # Return both features and the file name
        return features, os.path.basename(file_path)
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return None


def process_features(directory):
    files = [os.path.join(directory, f)
             for f in os.listdir(directory) if f.endswith('.mp3')]
    with ProcessPoolExecutor() as executor:
        features_list = list(executor.map(extract_features, files))
    # Filter out None results and separate features and file names
    features_list = [f for f in features_list if f is not None]
    if features_list:
        features_array = np.array([f[0] for f in features_list])
        scaler = StandardScaler()
        features_normalized = scaler.fit_transform(features_array)
        pca = PCA(n_components=0.95)
        features_reduced = pca.fit_transform(features_normalized)
        # Pair each reduced feature set with its file name
        return list(zip(features_reduced, [f[1] for f in features_list]))
    else:
        return []


def store_features(features):
    """ Store the features in the MongoDB collection with song names. """
    if len(features) > 0:
        documents = [{"features": feature[0].tolist(), "song_name": feature[1]}
                     for feature in features]
        collection.insert_many(documents)


if __name__ == '__main__':
    reduced_features = process_features(audio_dir)
    if len(reduced_features) > 0:
        store_features(reduced_features)
        logging.info("Features and song names stored successfully in MongoDB")
    else:
        logging.info("No features to store")

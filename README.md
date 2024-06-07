# Spotify-Clone

## Overview

The Spotify-Clone project focuses on implementing a music recommendation system, allowing users to experience playback, streaming capabilities, and real-time suggestions based on their activity. The system comprises three main files: `Feature_Extraction.py`, `Kafka_script.py`, and `spark_script.py` with associated `app.py' and 'Index.html` for the web interface.

## Contributors

- Jawad Ahmed
- Fasih Iqbal
- Hassan Rizwan

## Approach and Functionality

### Feature_Extraction.py

This phase involves extracting features from audio data and storing them in MongoDB. The process includes:

- Utilizing librosa for feature extraction like MFCCs, spectral centroids, and zero-crossing rates.
- Standardizing and reducing the extracted features using PCA.
- Storing the processed features in MongoDB for further analysis and model training.


### Kafka_script.py

This script facilitates real-time music recommendations using Kafka. The key functionalities include:

- Sending song names to a Kafka topic for recommendation processing.
- Listening for recommended songs from another Kafka topic and displaying them.
- Enabling interactive input for continuous song recommendation queries.

### spark_script.py

In this phase, a model is built to find similar songs using the Annoy library. The key steps include:

- Loading the audio features data from MongoDB into Spark.
- Building an Approximate Nearest Neighbors (ANN) index to find similar songs efficiently.
- Calculating cosine similarity between songs' feature vectors to recommend similar songs based on a selected input.

### App.py and Index.html

This part integrates the backend with a web interface using Flask. The functionality includes:

- Implementing a web interface for the Music Recommendation System.
- Connecting the backend processes with the front-end using Flask to provide seamless user experience.

### Real-Time Song Similarity

- The "Consumer" and "Producer" files along with the script file enable real-time updates for similar songs
- when a user plays a song, providing an interactive and dynamic user experience.

## Dependencies

The project relies on various libraries and tools such as:

- Python
- MongoDB
- librosa
- scikit-learn
- Annoy
- PySpark
- Flask

## Usage

1. **Feature Extraction**: Execute `Feature_Extraction.py` to extract and store audio features in MongoDB.
2. **Spark_script - Model Training**: Run `Spark_script.py` to build the model for recommending similar songs.
3. **Web Interface**: Start the application with Flask using `App.py` and access it through `Index.html` for user interaction.
4. **Real-Time Updates**: Utilize the "Consumer", "Producer", and associated script files to enable real-time song similarity updates based on user interactions.

Ensure you have the necessary dependencies installed to run the system successfully.

## Future Enhancements

- Incorporate user feedback for personalized recommendations.
- Enhance the user interface for a more engaging experience.

The README file provides an in-depth understanding of the Spotify-Clone project, its approach, functionality, and dependencies required for seamless execution. Feel free to further enhance and expand the project based on specific requirements and user feedback.

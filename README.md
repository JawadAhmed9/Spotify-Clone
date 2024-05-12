# Spotify-Clone

## Overview

The Spotify-Clone project focuses on implementing a music recommendation system, allowing users to experience playback, streaming capabilities, and real-time suggestions based on their activity. The system comprises three main files: `Phase1.py`, `Phase2.py`, and `App.py` with associated `Index.html` for the web interface.

## Contributors
- Fasih Iqbal
- Hassan Rizwan
- Jawad Ahmed

## Approach and Functionality

### Phase1.py
This phase involves extracting features from audio data and storing them in MongoDB. The process includes:
- Utilizing librosa for feature extraction like MFCCs, spectral centroids, and zero-crossing rates.
- Standardizing and reducing the extracted features using PCA.
- Storing the processed features in MongoDB for further analysis and model training.

### Phase2.py
In this phase, a model is built to find similar songs using the Annoy library. The key steps include:
- Loading the audio features data from MongoDB into Spark.
- Building an Approximate Nearest Neighbors (ANN) index to find similar songs efficiently.
- Calculating cosine similarity between songs' feature vectors to recommend similar songs based on a selected input.

### App.py and Index.html
This part integrates the backend with a web interface using Flask. The functionality includes:
- Implementing a web interface for the Music Recommendation System.
- Connecting the backend processes with the front-end using Flask to provide seamless user experience.

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

1. **Phase1 - Feature Extraction**: Execute `Phase1.py` to extract and store audio features in MongoDB.
2. **Phase2 - Model Training**: Run `Phase2.py` to build the model for recommending similar songs.
3. **Web Interface**: Start the application with Flask using `App.py` and access it through `Index.html` for user interaction.

Ensure you have the necessary dependencies installed to run the system successfully.

## Future Enhancements
- Incorporate user feedback for personalized recommendations.
- Enhance the user interface for a more engaging experience.


The README file provides an in-depth understanding of the Spotify-Clone project, its approach, functionality, and dependencies required for seamless execution. Feel free to further enhance and expand the project based on specific requirements and user feedback.  

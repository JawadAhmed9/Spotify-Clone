from flask import Flask, jsonify, request, send_from_directory, abort, render_template
import os
import random

app = Flask(__name__)

# Directory where your MP3 files are stored
MUSIC_FOLDER = r'C:\Users\PC\Documents\Symmester 4\Big Data\Assignment 4\data\BDS A\000'


@app.route('/')
def index():
    songs = [song for song in os.listdir(
        MUSIC_FOLDER) if song.endswith('.mp3')][:10]
    return render_template('index.html', songs=songs)


@app.route('/play/<path:filename>')
def stream_song(filename):
    try:
        if not filename.endswith('.mp3'):
            abort(404)  # Ensure the file is an mp3
        filename = os.path.join(MUSIC_FOLDER, filename)
        return send_from_directory(os.path.dirname(filename), os.path.basename(filename), as_attachment=False)
    except ValueError:
        abort(404)  # Handle unsafe file paths


@app.route('/similar/<song_name>')
def similar_songs(song_name):
    similar_songs = get_similar_songs(song_name)
    return jsonify(similar_songs)


def get_similar_songs(song_name):
    all_songs = [song for song in os.listdir(
        MUSIC_FOLDER) if song.endswith('.mp3') and song != song_name]
    similar_songs = random.sample(all_songs, min(
        5, len(all_songs)))
    return [{"name": song} for song in similar_songs]


if __name__ == '__main__':
    app.run(debug=True)

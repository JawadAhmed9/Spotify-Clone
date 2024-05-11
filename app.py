from flask import abort, Flask, render_template, jsonify, send_from_directory
from werkzeug.utils import safe_join
import os

app = Flask(__name__)

# Directory where your MP3 files are stored
MUSIC_FOLDER = r'C:\Users\PC\Documents\Symmester 4\Big Data\Assignment 4\data\BDS A\000'


def get_similar_songs(song_name):
    # Placeholder for fetching similar songs
    # Replace this logic with your actual method to retrieve similar songs
    return [{"name": "Song1"}, {"name": "Song2"}]  # Example format


@app.route('/')
def index():
    # List mp3 files from the music folder and limit to the first 10
    songs = [song for song in os.listdir(
        MUSIC_FOLDER) if song.endswith('.mp3')][:10]
    return render_template('index.html', songs=songs)


@app.route('/play/<path:filename>')
def stream_song(filename):
    try:
        # Ensure the file exists and is an mp3
        if not filename.endswith('.mp3'):
            abort(404)  # Not found if not an mp3 file
        filename = safe_join(MUSIC_FOLDER, filename)
        return send_from_directory(os.path.dirname(filename), os.path.basename(filename), as_attachment=False)
    except ValueError:
        abort(404)  # Not found if file path is unsafe


@app.route('/similar/<song_name>')
def similar_songs(song_name):
    similar_songs = get_similar_songs(song_name)
    return jsonify(similar_songs)  # Convert list of dicts to JSON


if __name__ == '__main__':
    app.run(debug=True)

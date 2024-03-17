from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

RAPIDAPI_KEY = "826e55dd55msha752e538e0a9226p1c8440jsnd18781c326b8"
RAPIDAPI_HOST = "genius-song-lyrics1.p.rapidapi.com"
SEARCH_URL = "https://genius-song-lyrics1.p.rapidapi.com/search/"
LYRICS_URL = "https://genius-song-lyrics1.p.rapidapi.com/song/lyrics/"

# Fungsi untuk menampilkan data pencarian
def display_search_results(data):
    hits = data.get('hits', [])
    results = []
    for hit in hits:
        result = hit.get('result', {})
        title = result.get('title', 'Unknown Title')
        artist = result.get('artist', 'Unknown Artist')
        release_date = result.get('release_date_for_display', 'Unknown Date')
        url = result.get('url', '#')
        results.append({
            'title': title,
            'artist': artist,
            'release_date': release_date,
            'url': url
        })
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "q": query,
        "per_page": "10",
        "page": "1"
    }
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    data = response.json()
    search_results = display_search_results(data)
    return render_template('results.html', results=search_results)


@app.route('/lyrics/<song_id>')
def lyrics(song_id):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "id": song_id
    }
    response = requests.get(LYRICS_URL, headers=headers, params=params)
    data = response.json()
    return render_template('lyrics.html', lyrics=data['lyrics'])

if __name__ == '__main__':
    app.run(debug=True)

import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- STRICT CONFIGURATION ---
# IMPORTANT: Replace with y" our actual 32-character API Key
API_KEY = "9291457166a815bac5769e279459fe7b"
TMDB_URL = "https://api.themoviedb.org/3"

# FIX part 1: Hardcode the image base URL here
IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_movie_data(endpoint, params={}):
    params.update({'api_key': API_KEY, 'language': 'hi-IN'})
    try:
        r = requests.get(f"{TMDB_URL}/{endpoint}", params=params, timeout=10)
        # Prevent crashes if API fails or Key is wrong
        if r.status_code != 200:
            return []
        return r.json().get('results', [])
    except:
        return []

@app.route('/')
def home():
    query = request.args.get('search')
    if query:
        # Multi-search handles both Movies and TV shows
        content = get_movie_data("search/multi", {"query": query})
    else:
        # Default: Trending Hindi Movies
        content = get_movie_data("discover/movie", {"with_original_language": "hi", "sort_by": "popularity.desc"})
    
    # FIX part 2: Explicitly pass 'img_base' to the template
    return render_template('index.html', content=content, img_base=IMG_BASE_URL)

@app.route('/watch/<m_type>/<m_id>')
def watch(m_type, m_id):
    # Fetch details for the watch page
    details = requests.get(f"{TMDB_URL}/{m_type}/{m_id}?api_key={API_KEY}&language=hi-IN").json()
    title = details.get('title') or details.get('name') or "Nawab Movie"
    
    # TV vs Movie Logic
    suffix = "/1/1" if m_type == "tv" else ""
    
    # Stable Server List
    sources = {
        "सर्वर 1 (Primary)": f"https://vidsrc.me/embed/{m_type}/{m_id}{suffix}",
        "सर्वर 2 (Alternative)": f"https://vidsrc.cc/v2/embed/{m_type}/{m_id}{suffix}",
        "सर्वर 3 (Hindi)": f"https://vidsrc.xyz/embed/{m_type}/{m_id}{suffix}"
    }
    
    return render_template('watch.html', sources=sources, title=title)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
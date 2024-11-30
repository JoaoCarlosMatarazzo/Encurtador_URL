import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.database import init_db, get_db
from backend.utils import generate_short_url, get_geolocation
import datetime

app = Flask(__name__)
db = init_db()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    if not original_url:
        return jsonify({"error": "URL is required"}), 400
    
    short_url = generate_short_url()
    db['urls'][short_url] = {"original_url": original_url, "clicks": 0, "click_data": []}
    return jsonify({"short_url": f"http://localhost:5000/{short_url}"}), 201

@app.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    url_data = db['urls'].get(short_url)
    if not url_data:
        return jsonify({"error": "URL not found"}), 404
    
    url_data['clicks'] += 1
    url_data['click_data'].append({
        "timestamp": datetime.datetime.now().isoformat(),
        "location": get_geolocation(request.remote_addr)
    })
    return jsonify({"redirect_to": url_data["original_url"]}), 302

@app.route('/metrics/<short_url>', methods=['GET'])
def get_metrics(short_url):
    url_data = db['urls'].get(short_url)
    if not url_data:
        return jsonify({"error": "URL not found"}), 404
    
    return jsonify({
        "original_url": url_data["original_url"],
        "clicks": url_data["clicks"],
        "click_data": url_data["click_data"]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

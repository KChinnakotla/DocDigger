from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/scrape/*": {"origins": "http://localhost:3000"}})

@app.route("/scrape", methods=["POST", "GET"])
def scrape():
    # data = request.get_json()
    url = request.args.get('url')
    url = url.strip("\"")

    if not url:
        return jsonify({"error": "URL not provided"}), 400

    visited = set()
    pdfs_obtained = set()
    urls_to_visit = [url]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    base_domain = urlparse(url).netloc

    while urls_to_visit:
        
        
        current_url = urls_to_visit.pop(0)
        
        
        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href)
                if href.endswith('.pdf'): 
                    if full_url not in pdfs_obtained:
                        print(full_url)
                        pdfs_obtained.add(full_url)
                elif urlparse(full_url).netloc == base_domain:
                    if full_url not in visited:
                        urls_to_visit.append(full_url)

        except Exception as e:
            print(f"Failed to process {current_url}: {e}")
    print("Done scraping")
    return jsonify({"pdfs": list(pdfs_obtained)})

if __name__ == '__main__':
    app.run(debug=True)

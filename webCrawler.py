import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Track visited URLs and PDFs
visited = set()
pdfs_obtained = set()
urls_to_visit = ["https://georgiaasyd.org/awards/"]

# Define headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

# Extract the base domain to restrict the crawling
base_domain = urlparse(urls_to_visit[0]).netloc

while urls_to_visit:
    url = urls_to_visit.pop(0)

    if url in visited:
        continue  # Skip already visited URLs
    
    visited.add(url)  # Mark the URL as visited
    
    try:
        # Send the request to get the contents of the webpage
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find and store all PDF links on the page
        for link in soup.find_all('a'):
            href = link.get('href')

            if href:
                full_url = urljoin(url, href)
                
                # Check if it's a PDF link and store it if new
                if href.endswith('.pdf') and full_url not in pdfs_obtained:
                    pdfs_obtained.add(full_url)
                    print(full_url)
                
                # Queue links within the same domain
                elif urlparse(full_url).netloc == base_domain and full_url not in visited:
                    urls_to_visit.append(full_url)

    except Exception as e:
        print(f"Failed to process {url}: {e}")

print("PDF scraping complete.")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Base URL to crawl
BASE_URL = "https://news.ycombinator.com"

# Keep track of visited pages
visited = set()

# Patterns to filter unwanted links
UNWANTED_PATTERNS = ["vote?id=", "hide?id=", "login?", "user?id=", "submit", "p=", "from?site="]

# Step 1: Start timer and fetch the main page
start_time = time.time()
response = requests.get(BASE_URL, timeout=5)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract unique links from the main page
links = set()
for a_tag in soup.find_all("a", href=True):
    full_url = urljoin(BASE_URL, a_tag["href"])  # Convert to absolute URL
    if full_url.startswith("http") and not any(pattern in full_url for pattern in UNWANTED_PATTERNS):
        links.add(full_url)

print(f"✅ Total Unique Links Found: {len(links)}")

# Dictionary to store the graph structure (page → outgoing links)
page_graph = {}

# Function to fetch page details and extract links
def fetch_page(url):
    """ Fetches a page, extracts title and links, prints progress, and returns them """
    if url in visited:
        print(f"🔄 Skipping already visited: {url}")
        return url, []

    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            print(f"⚠️ Skipping {url} (Status Code: {response.status_code})")
            return url, []

        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.title.string if soup.title else "No Title Found"
        print(f"🌍 [{len(visited)}/{len(links)}] Crawled: {page_title} | {url}")

        # Extract outgoing links
        page_links = set()
        for a_tag in soup.find_all("a", href=True):
            full_url = urljoin(url, a_tag["href"])
            if full_url.startswith("http") and full_url not in visited:
                page_links.add(full_url)

        return url, list(page_links)

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return url, []

# Step 3: Use multi-threading to fetch pages in parallel
MAX_THREADS = 10  # Adjust based on network speed & CPU

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    future_to_url = {executor.submit(fetch_page, url): url for url in links}

    for future in as_completed(future_to_url):
        url, found_links = future.result()
        page_graph[url] = found_links  # Store edges

# Save graph data to a JSON file
with open("graph_data.json", "w") as f:
    json.dump(page_graph, f, indent=4)

print("\n📁 Graph data saved to graph_data.json!")

# Step 4: Capture end time and print execution duration
end_time = time.time()
elapsed_time = end_time - start_time
print(f"\n⏳ Total Execution Time: {elapsed_time:.2f} seconds")

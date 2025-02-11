import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://news.ycombinator.com" 
visited = set() # Store Visited links
UNWANTED_PATTERNS = ["vote?id=", "hide?id=", "login?", "user?id=", "submit", "p=", "from?site="]

# Step 1: Fetch and parse the page
start_time = time.time()  # Start timer
response = requests.get(BASE_URL, timeout=5)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract and process all unique links before navigating
links = set()
for a_tag in soup.find_all("a", href=True):
    full_url = urljoin(BASE_URL, a_tag["href"]) # Convert to absolute URL
    if full_url.startswith("http") and not any(pattern in full_url for pattern in UNWANTED_PATTERNS):
        links.add(full_url)

print("Total Unique Links: ", len(links))

# Function to fetch page details
def fetch_page(url):
    if url in visited:
        return f"Skipping already visited: {url}"

    visited.add(url)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return f"Skipping {url} (Status Code: {response.status_code})"

        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.title.string if soup.title else "No Title Found"
        return f"Page Title: {page_title} | URL: {url}"

    except requests.exceptions.RequestException as e:
        return f"Failed to fetch {url}: {e}"


# Step 3: Use multi-threading to fetch pages in parallel
MAX_THREADS = 10  # Adjust this number based on network speed and CPU capacity

with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    future_to_url = {executor.submit(fetch_page, url): url for url in links}

    for future in as_completed(future_to_url):
        print(future.result())  # Print results as they complete

# Capture end time
end_time = time.time()
elapsed_time = end_time - start_time

# Print total execution time
print(f"\nTotal Execution Time: {elapsed_time:.2f} seconds")
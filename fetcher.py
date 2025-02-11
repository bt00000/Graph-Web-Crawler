import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://news.ycombinator.com" 
visited = set() # Store Visited links
UNWANTED_PATTERNS = ["vote?id=", "hide?id=", "login?", "user?id=", "submit", "p=", "from?site="]

# Step 1: Fetch and parse the page
response = requests.get(BASE_URL, timeout=5)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract and process all unique links before navigating
links = set()
for a_tag in soup.find_all("a", href=True):
    full_url = urljoin(BASE_URL, a_tag["href"]) # Convert to absolute URL
    if full_url.startswith("http") and not any(pattern in full_url for pattern in UNWANTED_PATTERNS):
        links.add(full_url)

print("Total Unique Links: ", len(links))

# Step 3: Loop through links
for i, next_url in enumerate(links):
    if next_url in visited:  # Avoid re-crawling visited URLs
        print(f"Skipping already visited: {next_url}")
        continue

    print(f"\n[{i+1}/{len(links)}] Navigating to: {next_url}")
    visited.add(next_url) # Mark as visited

    try:
        response = requests.get(next_url, timeout=5)
        if response.status_code !=200:
            print(f"Skipping {next_url} (Status Code: {response.status_code})")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Check if the title exists before trying to access it
        page_title = soup.title.string if soup.title else "No Title Found"
        print("Page Title:", page_title)

        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {next_url}: {e}")
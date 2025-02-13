import json
from collections import deque

# Load the web graph from JSON
with open("graph_data.json", "r") as f:
    graph = json.load(f)

def bfs(graph, start_url):
    """Perform BFS traversal on web graph."""

    queue = deque([start_url]) # Start from given URL
    visited = set() # Keep track of visited pages

    print("\n Starting BFS Traversal...\n")

    while queue: # While there are pages to visit
        node = queue.popleft() # Get the first element in queue (FIFO)

        if node not in visited:
            print(f"Visiting: {node}") # Print the current page
            visited.add(node) # Mark as visited

            # Add outgoing links (neighbors) to queue if not visited
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)

# Start BFS from a specific page (e.g., Hacker News)
if __name__ == "__main__":
    start_url = "https://news.ycombinator.com"
    bfs(graph, start_url)
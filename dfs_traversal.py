import csv
import json

# Load the web graph from JSON
with open("graph_data.json", "r") as f:
    graph = json.load(f)

def dfs(graph, start_url):
    """Perform DFS traversal on the web graph"""

    stack = [start_url]  # Start from given URL
    visited = set()  # Keep track of visited pages
    traversal_path = []  # Store traversal order

    print("\nStarting DFS Traversal...\n")

    while stack:  # While there are pages to visit
        node = stack.pop()  # Take the last added element (LIFO)

        if node not in visited:
            print(f"Visiting: {node}")  # Print the current page
            visited.add(node)  # Mark as visited
            traversal_path.append(node)  # Store visited URL

            # Add outgoing links (neighbors) to stack if not visited
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)

# Start DFS from a specific page (e.g., Hacker News)
if __name__ == "__main__":
    start_url = "https://news.ycombinator.com"
    dfs(graph, start_url)

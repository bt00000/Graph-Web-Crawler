import json
import networkx as nx

# Load graph data from JSON
with open("graph_data.json", "r") as f:
    page_graph = json.load(f)

# Create a Directed Graph
G = nx.DiGraph()

# Add nodes and edges
for page, links in page_graph.items():
    G.add_node(page)  # Add web page as a node
    for link in links:
        G.add_edge(page, link)  # Create a directed edge

print(f"Graph built with {len(G.nodes())} nodes and {len(G.edges())} edges.")

# Save the graph in Gephi-readable format
nx.write_gexf(G, "graph_data.gexf")
print("Graph saved as graph_data.gexf - Open in Gephi for visualization.")

import json
import networkx as nx
import matplotlib.pyplot as plt

# Load graph data from JSON
with open("graph_data.json", "r") as f:
    page_graph = json.load(f)

# Create a Directed Graph
G = nx.DiGraph()

# Add nodes and edges
for page, links in page_graph.items():
    G.add_node(page)
    for link in links:
        G.add_edge(page, link)

# **Step 1: Degree Distribution**
in_degrees = [G.in_degree(n) for n in G.nodes()]
out_degrees = [G.out_degree(n) for n in G.nodes()]

# print(in_degrees)
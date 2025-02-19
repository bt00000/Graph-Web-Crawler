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

# print(f"Total Pages: {len(G.nodes())}")
# print(f"Total Links: {len(G.edges())}")
# print(f"Max In-Degree: {max(in_degrees)}")
# print(f"Min In-Degree: {min(in_degrees)}")
# print(f"Average In-Degree: {sum(in_degrees)/len(in_degrees):.2f}")

# Plot In-Dgree Distribution
# plt.figure(figsize=(10, 5))
# plt.hist(in_degrees, bins=20, color='blue', alpha=0.7)
# plt.xlabel("In-Degree (Number of Incoming Links)")
# plt.ylabel("Frequency")
# plt.title("In-Degree Distribution of Web Pages")
# plt.show()

# # Plot Out-Degree Distribution
# plt.figure(figsize=(10, 5))
# plt.hist(out_degrees, bins=20, color='green', alpha=0.7)
# plt.xlabel("Out-Degree (Number of Outgoing Links)")
# plt.ylabel("Frequency")
# plt.title("Out-Degree Distribution of Web Pages")
# plt.show()

# **Step 2: Compute PageRank**
pagerank = nx.pagerank(G)

# Sort pages by PageRank value (highest to lowest)
top_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

# Print top pages by PageRank
print("\n Top 10 Most Important Pages (PageRank):")
for rank, (page, score) in enumerate(top_pages, start=1):
    print(f"{rank}. {page} -> Score: {score:.5f}")

# **Step 3: Identify Connected Components**
strong_components = list(nx.strongly_connected_components(G))
weak_components = list(nx.weakly_connected_components(G))

print(f"\n Total Strongly Connected Components: {len(strong_components)}")
print(f" Total Weakly Connected Components: {len(weak_components)}")

# Sort components by size
largest_weak_component = max(weak_components, key=len)

print(f"\n Largest Weakly Connected Component has {len(largest_weak_component)} pages.")

# Visualize component sizes
component_sizes = [len(comp) for comp in weak_components]

plt.figure(figsize=(10, 5))
plt.hist(component_sizes, bins=20, color='red', alpha=0.7)
plt.xlabel("Size of Weakly Connected Components")
plt.ylabel("Frequency")
plt.title("Distribution of Connected Component Sizes")
plt.show()
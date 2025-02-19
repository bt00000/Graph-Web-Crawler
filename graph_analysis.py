import json
import networkx as nx
import matplotlib.pyplot as plt
from urllib.parse import urlparse
from collections import defaultdict

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

# **Step 1: Degree Distribution Analysis**
in_degrees = [G.in_degree(n) for n in G.nodes()]
out_degrees = [G.out_degree(n) for n in G.nodes()]

print(f"\n📊 Graph Statistics:")
print(f"Total Pages: {len(G.nodes())}")
print(f"Total Links: {len(G.edges())}")
print(f"Max In-Degree: {max(in_degrees)}")
print(f"Min In-Degree: {min(in_degrees)}")
print(f"Average In-Degree: {sum(in_degrees) / len(in_degrees):.2f}")

# **Step 2: Improve PageRank Computation**
# **🔹 Remove Internal Navigation & Query Parameters**
internal_pages = {
    "https://news.ycombinator.com/submit",
    "https://news.ycombinator.com/jobs",
    "https://news.ycombinator.com/lists",
    "https://news.ycombinator.com/newest",
    "https://news.ycombinator.com/newcomments",
    "https://news.ycombinator.com/ask",
    "https://news.ycombinator.com/show",
    "https://news.ycombinator.com/from?site=ycombinator.com",
}

# **🔹 Remove Login, Hide, Favorite, and Other Query-Based URLs**
filtered_graph = G.copy()
for node in list(G.nodes()):
    if node in internal_pages or "?" in node:  # Removes query-based URLs
        filtered_graph.remove_node(node)

# **🔹 Remove Orphan Pages (Pages with No Incoming Links)**
orphan_nodes = [node for node in filtered_graph.nodes if filtered_graph.in_degree(node) == 0]
filtered_graph.remove_nodes_from(orphan_nodes)

# **🔹 Compute PageRank with Standard Damping Factor (0.85)**
pagerank = nx.pagerank(filtered_graph, alpha=0.85)

# **Sort Pages by PageRank Score**
top_pages = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

# **Print Top 10 Important Pages**
print("\n🏆 Top 10 Most Important Pages (Filtered PageRank):")
for rank, (page, score) in enumerate(top_pages, start=1):
    print(f"{rank}. {page} -> Score: {score:.5f}")

# **Step 3: Identify Connected Components**
strong_components = list(nx.strongly_connected_components(G))
weak_components = list(nx.weakly_connected_components(G))

print(f"\n🔗 Total Strongly Connected Components: {len(strong_components)}")
print(f"🔗 Total Weakly Connected Components: {len(weak_components)}")

# **Find Largest Weakly Connected Component**
largest_weak_component = max(weak_components, key=len)
print(f"\n🔥 Largest Weakly Connected Component has {len(largest_weak_component)} pages.")

# **Step 4: Find Most Influential Domains**
domain_pagerank = defaultdict(float)

for page, score in pagerank.items():
    domain = urlparse(page).netloc
    domain_pagerank[domain] += score

# **Sort Domains by Total PageRank Score**
top_domains = sorted(domain_pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

# **Print Top Domains by Influence**
print("\n🌎 Top 10 Most Influential Domains (Aggregated PageRank):")
for rank, (domain, score) in enumerate(top_domains, start=1):
    print(f"{rank}. {domain} -> Score: {score:.5f}")


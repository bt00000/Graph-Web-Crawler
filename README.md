![image](https://github.com/user-attachments/assets/f0828f2d-8c53-4286-b05a-ca45d69059bb)
# Web Graph Analysis & Visualization

This project **crawls web pages**, builds a **directed graph** of linked pages, and analyzes their connectivity using **graph algorithms** like **BFS, DFS, PageRank, and Connected Components**. It also visualizes the graph in **Gephi** for deeper insights.

---

## Project Structure

```
Graph-Web-Crawler
│── README.md                 # Project Documentation
│── fetcher.py                 # Web Crawler to collect links
│── bfs.py                      # BFS Traversal
│── dfs.py                      # DFS Traversal
│── graph_analysis.py           # Graph Analysis (PageRank, Components)
│── graph_data.json             # Crawled Web Graph Data
│── graph_visualization.gexf    # Graph File for Gephi
```

---

## ⚙Installation & Setup

### Clone the Repository

```sh
git clone https://github.com/bt00000/Graph-Web-Crawler.git
cd graph-web-crawler
```

### Install Dependencies

Make sure you have Python installed. Then install required packages:

```sh
pip install -r requirements.txt
```

### Run the Web Crawler

To fetch and build the web graph:

```sh
python fetcher.py
```

This generates `graph_data.json`, containing the web structure.

---

## Usage

### Run BFS Traversal

```sh
python bfs.py
```

- **Outputs**: `bfs_traversal.csv`

### Run DFS Traversal

```sh
python dfs.py
```

- **Outputs**: `dfs_traversal.csv`

### Analyze & Rank Web Pages

```sh
python graph_analysis.py
```

- Computes **PageRank**, **Connected Components**, and **Degree Distribution**.
- Saves graphs for **Gephi visualization** (`graph_data.gexf`).

---

## Visualizing in Gephi


https://github.com/user-attachments/assets/36d2cab0-ef22-4297-8e4e-2bc834f49397


1. Open **Gephi** and load `graph_data.gexf`.
2. Apply **ForceAtlas2** layout for better visualization.
3. Use **Partition → PageRank** to color important nodes.
4. Explore **weakly & strongly connected components**.

---

## Key Features

**Web Crawling**: Extracts links from a seed website.  
**Graph Construction**: Builds a **directed graph** of web pages.  
**Graph Traversal**: Implements **BFS** & **DFS** to explore pages.  
**PageRank Algorithm**: Ranks the most important pages.  
**Connected Components Analysis**: Finds **largest** and **isolated** page clusters.  
**Gephi Visualization**: Export graphs for interactive exploration.  

---

## Future Improvements

Expand crawling depth  
Integrate sentiment analysis of page content  
Optimize PageRank with real-time updates  
Add topic-based filtering  

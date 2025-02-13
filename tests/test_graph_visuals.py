#!/usr/bin/env python
"""
Test: test_graph_visuals.py

These test cases load a network in to a plotly graph for browser rendering.
"""

# Import modules and config
from src.visualization.graph_plotter import generate_3d_network_figure
from src.network.network_builder import load_network
from src.network.community_builder import load_communities
from config import PROJECT_ROOT


graph_file_path = PROJECT_ROOT / "data" / "processed" / "network.gexf"
communities_file_path = PROJECT_ROOT / "data" / "processed" / "communities.json"

# Load the network graph and communities mapping from file.
G = load_network(str(graph_file_path))
communities = load_communities(str(communities_file_path))

fig = generate_3d_network_figure(G, communities=communities)
fig.show(renderer='browser')

print("Graph rendered...")

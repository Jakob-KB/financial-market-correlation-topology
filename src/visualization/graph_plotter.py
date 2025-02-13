#!/usr/bin/env python
"""
Module: graph_plotter.py

This module provides functions to generate 3D visualizations using Plotly:
specifically, it creates a 3D network visualization from a NetworkX graph.
"""

import networkx as nx
import plotly.graph_objects as go

from src.utils.setup_logger import setup_logger
from config import GRAPH_CONFIG

# Configure module-level logger
logger = setup_logger(__name__, log_to_console=False)


def generate_3d_network_figure(G: nx.Graph, communities: dict = None, seed: int = 42) -> go.Figure:
    """
    Generate an interactive 3D network visualization from a NetworkX graph.

    If a communities mapping is provided, each node is colored based on its community.

    Args:
        G (nx.Graph): The NetworkX graph to visualize.
        communities (dict, optional): Mapping from node to community index.
        seed (int, optional): Random seed for layout consistency. Defaults to 42.

    Returns:
        go.Figure: A Plotly Figure object representing the 3D network visualization.
    """
    # Compute node positions
    try:
        pos = GRAPH_CONFIG.LAYOUT_FUNC(G, dim=GRAPH_CONFIG.DIM, seed=GRAPH_CONFIG.SEED, k=GRAPH_CONFIG.K)
    except AttributeError:
        logger.warning(f"Invalid layout function in config. Using default layout from config.")
        pos = nx.spring_layout(G, dim=GRAPH_CONFIG.DIM, seed=GRAPH_CONFIG.SEED, k=GRAPH_CONFIG.K)

    # Prepare lists for node positions and colors
    node_x, node_y, node_z = [], [], []
    node_text = []
    node_colors = []

    color_mapping = None

    # If a communities mapping is provided, create a color palette for communities
    if communities:
        # Import plotly colors if communities need to be differentiated
        from plotly.colors import qualitative

        palette = qualitative.Plotly
        unique_communities = sorted(set(communities.values()))
        color_mapping = {
            community: palette[i % len(palette)]
            for i, community in enumerate(unique_communities)
        }

    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(str(node))
        if communities and color_mapping:
            node_colors.append(color_mapping[communities[node]])
        else:
            # Fallback node color
            node_colors.append("blue")

    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode="markers+text",
        marker=dict(
            size=GRAPH_CONFIG.NODE_SIZE,
            color=node_colors,
            showscale=False,  # Hide node degree color-bar since displaying nodes using community colors
        ),
        text=node_text,
        hoverinfo="text",
    )

    # Build edge traces for 3D lines
    edge_x, edge_y, edge_z = [], [], []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(color="grey", width=1),
        opacity=GRAPH_CONFIG.EDGE_OPACITY,
        hoverinfo="none",
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text="3D Network Visualization", font=dict(size=16)),
            showlegend=False,
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        ),
    )

    logger.info("Node positing calculated and figure drawn.")
    return fig

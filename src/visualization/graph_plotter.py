#!/usr/bin/env python
"""
Module: graph_plotter.py

This module provides functions to generate 3D visualizations using Plotly:
specifically, it creates a 3D network visualization from a NetworkX graph.
"""

from typing import Optional, Dict

import networkx as nx
import plotly.graph_objects as go

from config import GRAPH_CONFIG
from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__)


def generate_3d_network_figure(
        G: nx.Graph,
        communities: Optional[Dict] = None,
        layout_func=GRAPH_CONFIG.LAYOUT_FUNC,
        dim: int = GRAPH_CONFIG.DIM,
        k: float = GRAPH_CONFIG.K,
        seed: int = GRAPH_CONFIG.SEED,
        node_size: int = GRAPH_CONFIG.NODE_SIZE,
        edge_opacity: float = GRAPH_CONFIG.EDGE_OPACITY
) -> go.Figure:
    """
    Generate an interactive 3D network visualization from a NetworkX graph.

    If a communities mapping is provided, each node is colored based on its community.
    Defaults to using layout and styling parameters from GRAPH_CONFIG, but these
    can be overridden via function arguments.

    Args:
        G (nx.Graph): The NetworkX graph to visualize.
        communities (dict, optional): Mapping of node → community index.
        layout_func (Callable): Layout function for positioning nodes (e.g., nx.spring_layout).
        dim (int): Dimensionality of the layout (e.g., 3 for 3D).
        k (float): Optimal distance between nodes in the layout algorithm.
        seed (int): Random seed for layout consistency.
        node_size (int): Size of the plotted nodes.
        edge_opacity (float): Opacity for the plotted edges.

    Returns:
        go.Figure: A Plotly Figure object representing the 3D network visualization.
    """

    # Compute node positions
    try:
        pos = layout_func(G, dim=dim, seed=seed, k=k)
    except (AttributeError, TypeError) as e:
        logger.warning("Invalid layout function or parameters. Falling back to spring_layout. Error: %s", e)
        pos = nx.spring_layout(G, dim=dim, seed=seed, k=k)

    # Prepare lists for node positions and colors
    node_x, node_y, node_z = [], [], []
    node_text = []
    node_colors = []

    # Construct color mapping if communities are provided
    color_mapping = None
    if communities:
        from plotly.colors import qualitative
        palette = qualitative.Plotly
        unique_communities = sorted(set(communities.values()))
        color_mapping = {
            community: palette[i % len(palette)] for i, community in enumerate(unique_communities)
        }

    # Populate node positions and colors
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        node_text.append(str(node))

        if communities and color_mapping:
            node_colors.append(color_mapping.get(communities.get(node), "blue"))
        else:
            node_colors.append("blue")  # Fallback node color

    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode="markers+text",
        marker=dict(
            size=node_size,
            color=node_colors,
            showscale=False  # Hide colorbar because colors are from communities
        ),
        text=node_text,
        hoverinfo="text"
    )

    # Build edge traces
    edge_x, edge_y, edge_z = [], [], []
    for src, dst in G.edges():
        x0, y0, z0 = pos[src]
        x1, y1, z1 = pos[dst]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    edge_trace = go.Scatter3d(
        x=edge_x,
        y=edge_y,
        z=edge_z,
        mode="lines",
        line=dict(color="grey", width=1),
        opacity=edge_opacity,
        hoverinfo="none"
    )

    # Assemble the figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=dict(text="3D Network Visualization", font=dict(size=16)),
            showlegend=False,
            scene=dict(
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                zaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
    )

    logger.info("3D network figure generated with %d nodes and %d edges.", G.number_of_nodes(), G.number_of_edges())
    return fig

#!/usr/bin/env python
"""
Module: community_builder.py

This module provides functions to perform community detection (clustering) on a stock correlation network.
It uses a greedy modularity maximization algorithm to partition the network into communities.
It also provides functions to save and load the community mapping as JSON.
"""

import json
import os
from typing import Optional

import networkx as nx

from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__, add_console=False)


def detect_communities(G: nx.Graph) -> Optional[dict]:
    """
    Detect communities in the correlation network using a greedy modularity maximization algorithm.

    This function uses NetworkX's greedy_modularity_communities function to partition the graph.
    It returns a dictionary mapping each node to its community index.

    Args:
        G (nx.Graph): The correlation network.

    Returns:
        Optional[dict]: A dictionary mapping each node (ticker) to its community index,
                        or None if community detection fails.
    """
    try:
        from networkx.algorithms.community import greedy_modularity_communities

        communities = greedy_modularity_communities(G)
        community_map = {}
        for idx, community in enumerate(communities):
            for node in community:
                community_map[node] = idx
        logger.info("Detected %d communities in the network.", len(communities))
        return community_map
    except Exception as e:
        logger.error("Community detection failed: %s", e)
        return None


def save_communities(communities: dict, filename: str) -> None:
    """
    Save the community mapping to a JSON file.

    Args:
        communities (dict): A dictionary mapping nodes to community indices.
        filename (str): The file path where the JSON will be saved.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(communities, f, indent=4)
        logger.info("Community mapping saved to %s.", filename)
    except Exception as e:
        logger.error("Failed to save community mapping: %s", e)


def load_communities(filename: str) -> dict:
    """
    Load the community mapping from a JSON file.

    Args:
        filename (str): The file path from which to load the community mapping.

    Returns:
        dict: The community mapping.
    """
    try:
        with open(filename, "r") as f:
            communities = json.load(f)
        logger.info("Community mapping loaded from %s.", filename)
        return communities
    except Exception as e:
        logger.error("Failed to load community mapping: %s", e)
        raise e

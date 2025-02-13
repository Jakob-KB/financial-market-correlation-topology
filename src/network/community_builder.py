#!/usr/bin/env python
"""
Module: community_builder.py

This module provides functions to perform community detection (clustering) on a stock correlation network.
It uses a greedy modularity maximization algorithm to partition the network into communities.
It also provides functions to save and load the community mapping as JSON.
"""

import json
from pathlib import Path
from typing import Optional

import networkx as nx

from config import DIRECTORY_CONFIG
from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__)


def detect_communities(G: nx.Graph) -> Optional[dict]:
    """
    Detect communities in the correlation network using a greedy modularity maximization algorithm.

    This function leverages NetworkX's greedy_modularity_communities to partition the graph.
    It returns a dictionary mapping each node (ticker) to its community index.

    Args:
        G (nx.Graph): The correlation network graph.

    Returns:
        Optional[dict]: Mapping node → community index, or None if detection fails.
    """
    try:
        from networkx.algorithms.community import greedy_modularity_communities
        communities = greedy_modularity_communities(G)
        community_map = {node: idx for idx, community in enumerate(communities) for node in community}
        logger.info("Detected %d communities in the network.", len(communities))
        return community_map
    except Exception as e:
        logger.error("Community detection failed: %s", e)
        return None


def save_communities(
    communities: dict,
    file_name: str,
    output_dir: Path = DIRECTORY_CONFIG.PROCESSED_DATA_DIR
) -> None:
    """
    Save the community mapping to a JSON file.

    Args:
        communities (dict): A dictionary mapping nodes to community indices.
        file_name (str): Name of the JSON file to be saved.
        output_dir (Path): Directory where the JSON file will be stored.

    Returns:
        None
    """
    file_path = output_dir / file_name
    try:
        with file_path.open("w") as f:
            json.dump(communities, f, indent=4)
        logger.info("Saved community mapping to %s.", file_path)
    except Exception as e:
        logger.error("Failed to save community mapping to %s: %s", file_path, e)


def load_communities(
    file_name: str,
    input_dir: Path = DIRECTORY_CONFIG.PROCESSED_DATA_DIR
) -> dict:
    """
    Load the community mapping from a JSON file.

    Args:
        file_name (str): Name of the JSON file storing communities.
        input_dir (Path): Directory where the JSON file is stored.

    Returns:
        dict: The community mapping (node → community index).

    Raises:
        Exception: If loading the file fails for any reason.
    """
    file_path = input_dir / file_name
    try:
        with file_path.open("r") as f:
            communities = json.load(f)
        logger.info("Loaded community mapping from %s.", file_path)
        return communities
    except Exception as e:
        logger.error("Failed to load community mapping from %s: %s", file_path, e)
        raise e

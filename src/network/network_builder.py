#!/usr/bin/env python
"""
Module: network_builder.py

This module provides functions to build and analyze a stock correlation network using a correlation matrix.
Each node in the graph represents a stock, and an edge is added between two stocks if the absolute correlation
between them exceeds a specified threshold. Edge weights are set to the corresponding correlation value.

It also provides functions to save and load the network data in GEXF format.
"""

from pathlib import Path

import networkx as nx
import pandas as pd

from config import DATA_CONFIG, DIRECTORY_CONFIG
from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__)


def build_correlation_network(
    correlation_matrix: pd.DataFrame,
    threshold: float = DATA_CONFIG.CORRELATION_THRESHOLD
) -> nx.Graph:
    """
    Build a correlation network from a given correlation matrix.

    Each node represents a stock (identified by its ticker). An edge is added between two stocks
    if the absolute correlation between them is >= `threshold`. The edge weight is the correlation value.

    Args:
        correlation_matrix (pd.DataFrame): A square DataFrame of pairwise correlation values.
        threshold (float): Minimum absolute correlation needed to add an edge (default 0.5).

    Returns:
        nx.Graph: Undirected graph representing the correlation network.

    Raises:
        ValueError: If the provided correlation_matrix is empty.
    """
    if correlation_matrix.empty:
        logger.error("The correlation matrix is empty.")
        raise ValueError("Correlation matrix must not be empty.")

    # Initialize graph
    G = nx.Graph()
    tickers = correlation_matrix.columns.tolist()

    logger.info("Adding %d nodes to the network.", len(tickers))
    G.add_nodes_from(tickers)

    # Add edges based on threshold
    n_edges = 0
    for i, ticker1 in enumerate(tickers):
        for ticker2 in tickers[i + 1:]:
            corr_value = correlation_matrix.loc[ticker1, ticker2]
            if abs(corr_value) >= threshold:
                G.add_edge(ticker1, ticker2, weight=corr_value)
                n_edges += 1

    logger.info("Added %d edges using threshold = %.2f.", n_edges, threshold)
    return G


def save_network(
    G: nx.Graph,
    file_name: str,
    output_dir: Path = DIRECTORY_CONFIG.PROCESSED_DATA_DIR
) -> None:
    """
    Save the network graph to a file in GEXF format.

    Args:
        G (nx.Graph): The network graph to save.
        file_name (str): Name of the network file.
        output_dir (Path): Location where the GEXF file will be saved.

    Returns:
        None
    """
    file_path = output_dir / file_name
    try:
        nx.write_gexf(G, file_path)
        logger.info("Saved network graph to %s.", file_path)
    except Exception as e:
        logger.error("Failed to save network graph to %s: %s", file_path, e)


def load_network(
    file_name: str,
    input_dir: Path = DIRECTORY_CONFIG.PROCESSED_DATA_DIR
) -> nx.Graph:
    """
    Load a network graph from a GEXF file.

    Args:
        file_name (str): Name of the network file.
        input_dir (Path): Location where the GEXF file is saved.

    Returns:
        nx.Graph: The loaded network graph.

    Raises:
        Exception: If the GEXF file cannot be read for any reason.
    """
    file_path = input_dir / file_name
    try:
        G = nx.read_gexf(file_path)
        logger.info("Loaded network graph from %s.", file_path)
        return G
    except Exception as e:
        logger.error("Failed to load network graph from %s: %s", file_path, e)
        raise e

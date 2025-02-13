#!/usr/bin/env python
"""
Module: network_builder.py

This module provides functions to build and analyze a stock correlation network using a correlation matrix.
Each node in the graph represents a stock, and an edge is added between two stocks if the absolute correlation
between them exceeds a specified threshold. Edge weights are set to the corresponding correlation value.
It also provides functions to save and load the network data.
"""

import os
import networkx as nx
import pandas as pd

from src.utils.setup_logger import setup_logger

# Configure module-level logger
logger = setup_logger(__name__, log_to_console=False)


def build_correlation_network(correlation_matrix: pd.DataFrame, threshold: float = 0.5) -> nx.Graph:
    """
    Build a correlation network from a given correlation matrix.

    Each node represents a stock (identified by its ticker). An edge is added between two stocks if the absolute
    correlation between them is greater than or equal to the specified threshold. The edge weight is the correlation
    value.

    Args:
        correlation_matrix (pd.DataFrame): A square DataFrame containing pairwise correlation values.
        threshold (float, optional): Minimum absolute correlation required to add an edge. Defaults to 0.5.

    Returns:
        nx.Graph: An undirected graph representing the correlation network.
    """
    if correlation_matrix.empty:
        logger.error("The correlation matrix is empty.")
        raise ValueError("Correlation matrix must not be empty.")

    G = nx.Graph()
    tickers = correlation_matrix.columns.tolist()
    logger.info("Adding %d nodes to the network.", len(tickers))
    G.add_nodes_from(tickers)

    n_edges = 0
    for i, ticker1 in enumerate(tickers):
        for ticker2 in tickers[i + 1:]:
            corr_value = correlation_matrix.loc[ticker1, ticker2]
            if abs(corr_value) >= threshold:
                G.add_edge(ticker1, ticker2, weight=corr_value)
                n_edges += 1

    logger.info("Added %d edges to the network with threshold %s.", n_edges, threshold)
    return G


def save_network(G: nx.Graph, filename: str) -> None:
    """
    Save the network graph to a file in GEXF format.

    Args:
        G (nx.Graph): The network graph to save.
        filename (str): The file path where the graph will be saved.
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        nx.write_gexf(G, filename)
        logger.info("Network graph saved to network.gexf")
    except Exception as e:
        logger.error("Failed to save network graph: %s", e)


def load_network(filename: str) -> nx.Graph:
    """
    Load a network graph from a GEXF file.

    Args:
        filename (str): The file path from which to load the graph.

    Returns:
        nx.Graph: The loaded network graph.
    """
    try:
        G = nx.read_gexf(filename)
        logger.info("Network graph loaded from %s.", filename)
        return G
    except Exception as e:
        logger.error("Failed to load network graph: %s", e)
        raise e

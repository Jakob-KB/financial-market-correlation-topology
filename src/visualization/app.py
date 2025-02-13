#!/usr/bin/env python
"""
Module: app.py

This Dash application creates an interactive dashboard for visualizing the stock correlation network.
It utilizes the following modules:
    - network_builder (to construct the network from a correlation matrix),
    - community_builder (to detect communities),
    - graph_plotter (to generate an interactive Plotly 3D network figure).
"""

from pathlib import Path

import dash
from dash import dcc, html, Input, Output
import pandas as pd

from config import DIRECTORY_CONFIG, APP_CONFIG, DATA_CONFIG
from src.network.network_builder import build_correlation_network
from src.network.community_builder import detect_communities
from src.visualization.graph_plotter import generate_3d_network_figure

# Define the path for the processed correlation matrix
CORR_MATRIX_FILE = Path(DIRECTORY_CONFIG.PROCESSED_DATA_DIR) / "correlation_matrix.csv"

# Load the correlation matrix
corr_matrix = pd.read_csv(CORR_MATRIX_FILE, index_col=0)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Interactive Stock Correlation Network"

# Define the layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1("Interactive Stock Correlation Network", style={"textAlign": "center"}),
                html.Div(
                    children=[
                        html.Label("Correlation Threshold:"),
                        dcc.Slider(
                            id="threshold-slider",
                            min=0.0,
                            max=1.0,
                            step=APP_CONFIG.CORRELATION_THRESHOLD_STEP,
                            value=DATA_CONFIG.CORRELATION_THRESHOLD,
                            marks={i / 10: f"{i / 10:.1f}" for i in range(0, 11)},
                        ),
                    ],
                    style={"width": "80%", "margin": "auto", "padding": "20px"},
                ),
            ],
            style={"flex": "0 0 auto"},
        ),
        html.Div(
            children=[dcc.Graph(id="network-graph", style={"width": "100%", "height": "100%"})],
            style={"flex": "1 1 auto"},
        ),
    ],
    style={"display": "flex", "flexDirection": "column", "height": "100vh", "margin": "0", "padding": "0"},
)


@app.callback(Output("network-graph", "figure"), Input("threshold-slider", "value"))
def update_network(threshold: float):
    """
    Update the network graph based on the selected threshold.

    Args:
        threshold (float): The correlation threshold value from the slider.

    Returns:
        plotly.graph_objs._figure.Figure: The updated 3D network figure.
    """
    G = build_correlation_network(correlation_matrix=corr_matrix, threshold=threshold)
    communities = detect_communities(G)
    fig = generate_3d_network_figure(G=G, communities=communities)
    return fig


def run_native_app():
    app.run_server(debug=False)


if __name__ == "__main__":
    run_native_app()

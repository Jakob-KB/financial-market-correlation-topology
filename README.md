# Financial Market Correlation Topology

Visualizing stock correlations using a dynamic, interactive network graph.

## Overview

This project builds an **interactive 3D network graph** to visualize stock correlations. The pipeline follows these steps:

1. **Download historical stock data** using `yfinance`.
2. **Process stock data** to compute daily returns and a correlation matrix.
3. **Build a correlation network**, connecting stocks based on correlation strength.
4. **Detect stock clusters (communities)** using network analysis.
5. **Generate an interactive 3D visualization** with `Plotly`.

## Project Structure

```
InteractiveStockCorrelationNetwork/
│── src/
│   ├── data/
│   │   ├── data_loader.py  # Downloads stock data from yfinance
│   │   ├── data_processor.py  # Calculates daily returns & correlation matrix
│   ├── network/
│   │   ├── network_builder.py  # Constructs the correlation network
│   │   ├── community_builder.py  # Detects stock clusters (communities)
│   ├── visualization/
│   │   ├── graph_plotter.py  # Generates the 3D interactive network graph
│   │   ├── app.py  # Dash web app for visualization
│   ├── utils/
│   │   ├── setup_logger.py  # Logging setup
│   ├── main.py  # Runs the entire pipeline
│
│── data/  # Stores raw & processed stock data
│── logs/  # Logs for debugging
│── config.py  # Configuration (dates, thresholds, etc.)
│── requirements.txt  # Dependencies
│── README.md  # Project documentation
```

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/InteractiveStockCorrelationNetwork.git
cd InteractiveStockCorrelationNetwork
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Settings (Optional)
Modify **`config.py`** to adjust parameters such as:
- Stock tickers
- Date range
- Correlation threshold
- Graph layout options

## Usage

### Run the Full Pipeline
```bash
python src/main.py
```
This will:
- Download stock data
- Compute the correlation matrix
- Build and save the correlation network
- Detect stock clusters
- Generate an interactive 3D graph

### Run the Dash Web App
```bash
python src/visualization/app.py
```
Open `http://127.0.0.1:8050/` in your browser to interact with the network.

## Features

- **Customizable stock tickers & timeframes**
- **Modular pipeline for easy expansion**
- **Network clustering with community detection**
- **Multiple graph layouts (spring, Kamada-Kawai, Fruchterman-Reingold)**
- **Optimized performance with caching & logging**
- **Interactive 3D visualization with Plotly**

## Technologies Used

- **Python** (Core logic)
- **`yfinance`** (Stock data API)
- **`pandas`** (Data processing)
- **`networkx`** (Graph/network analysis)
- **`plotly`** (3D visualization)
- **`Dash`** (Web interface)

## License

This project is open-source under the **MIT License**.

## Contact

For questions or contributions, reach out at **jakob.kb@outlook.com**.

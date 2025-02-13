# Financial Market Correlation Topology

Visualizing stock correlations using a dynamic, interactive network graph

## 📌 Overview
This project builds an **interactive 3D network graph** to visualize correlations between stocks. It follows a **pipeline** to:
1. **Download historical stock data** from `yfinance`
2. **Process stock data** to compute daily returns and a **correlation matrix**
3. **Build a correlation network**, where stocks are connected based on their correlation strength
4. **Detect stock clusters (communities)** using network analysis
5. **Generate an interactive 3D visualization** using `Plotly`

---

## 📂 Project Structure
```
InteractiveStockCorrelationNetwork/
│── src/
│   ├── data/
│   │   ├── data_loader.py  # Downloads stock data from yfinance
│   │   ├── data_processor.py  # Calculate daily returns & correlation matrix
│   ├── network/
│   │   ├── network_builder.py  # Constructs the correlation network
│   │   ├── community_builder.py  # Detects stock communities (clusters)
│   ├── visualization/
│   │   ├── graph_plotter.py  # Generates the 3D interactive network graph
│   │   ├── app.py  # Dash web app to visualize the network
│   ├── utils/
│   │   ├── setup_logger.py  # Logging setup
│   ├── main.py  # Runs the entire pipeline
│
│── data/  # Stores raw & processed stock data
│── logs/  # Logs for debugging
│── config.py  # Configurable parameters (dates, thresholds, etc.)
│── requirements.txt  # Dependencies
│── README.md  # Project documentation
```

---

## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/InteractiveStockCorrelationNetwork.git
cd InteractiveStockCorrelationNetwork
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Settings (Optional)
Modify **`config.py`** to adjust parameters like:
- Default tickers
- Start & end dates
- Correlation threshold
- Graph layout

---

## 🚀 Usage
### Run the Full Pipeline
```bash
python src/main.py
```
This will:
* Download stock data  
* Process and save the correlation matrix  
* Build & save the stock correlation network  
* Detect stock clusters  
* Display the interactive 3D graph  

### Run the Dash Web App
```bash
python src/visualization/app.py
```
📊 **Visit**: `http://127.0.0.1:8050/` in your browser to interact with the network.

---

## ⚙️ Features
* **Customizable stock tickers & timeframes**  
* **Modularized pipeline for easy expansion**  
* **Network clustering with community detection**  
* **Multiple graph layouts (spring, Kamada-Kawai, Fruchterman-Reingold)**  
* **Optimized for performance (tqdm, caching, logging)**  
* **Interactive 3D visualization with Plotly**  

---

## 🛠️ Technologies Used
- **Python** (Core logic)
- **`yfinance`** (Stock data API)
- **`pandas`** (Data processing)
- **`networkx`** (Graph/network analysis)
- **`plotly`** (3D visualization)
- **`Dash`** (Web interface)

---

## 📜 License
📝 MIT License. Feel free to modify and use this project.

---

## 🤝 Contributing
PRs & suggestions are welcome! Fork the repo and open an issue.

📩 **Contact**: jakob.kb@outlook.com  


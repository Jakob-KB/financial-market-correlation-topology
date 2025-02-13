# config.py
from dataclasses import dataclass, field
from typing import List

from pathlib import Path

# Compute the absolute path to the project root.
PROJECT_ROOT = Path(__file__).resolve().parent

# Define directories relative to the project root
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample_tickers"
LOGS_DIR = PROJECT_ROOT / "logs"
SRC_ROOT = PROJECT_ROOT / "src"


# Graph config
@dataclass(frozen=True)
class GraphConfig:
    COLOURING_MODE: str = 'community_colouring'
    POSITIONING_LAYOUT: str = 'spring_layout'
    NODE_SIZE: int = 8
    EDGE_OPACITY: float = 0.6


# Default args for demoing modules
@dataclass(frozen=True)
class DefaultArguments:
    DEFAULT_TICKERS: List[str] = field(default_factory=lambda: ["AAPL", "MSFT", "GOOGL", "AMZN"])
    DEFAULT_START_DATE: str = "2020-01-01"
    DEFAULT_END_DATE: str = "2024-01-01"
    DEFAULT_INTERVAL: str = "1d"
    DEFAULT_CORRELATION_THRESHOLD: float = 0.5


# Create a singleton instances for easy access
DEFAULT_ARGUMENTS = DefaultArguments()
GRAPH_CONFIG = GraphConfig()

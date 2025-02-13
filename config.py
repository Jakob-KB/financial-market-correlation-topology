# config.py
from dataclasses import dataclass, field
from typing import List, Callable
import networkx as nx
from pathlib import Path
import logging

# Compute the absolute path to the project root.
PROJECT_ROOT = Path(__file__).resolve().parent

# Graph config
@dataclass(frozen=True)
class GraphConfig:
    # General
    COLOURING_MODE: str = 'community_colouring'
    NODE_SIZE: int = 8
    EDGE_OPACITY: float = 0.6

    # Graph layout positioning
    SEED: int = 42
    K: float = 0.3
    DIM: int = 3

    # Layout function reference (spring_layout, kamada_kawai_layout or fruchterman_reingold_layout)
    LAYOUT_FUNC: Callable = nx.spring_layout


# Default args for demoing modules
@dataclass(frozen=True)
class DefaultArguments:
    DEFAULT_TICKERS: List[str] = field(default_factory=lambda: ["AAPL", "MSFT", "GOOGL", "AMZN"])
    DEFAULT_START_DATE: str = "2020-01-01"
    DEFAULT_END_DATE: str = "2024-01-01"
    DEFAULT_INTERVAL: str = "1d"
    DEFAULT_CORRELATION_THRESHOLD: float = 0.5


# Logger config
@dataclass(frozen=True)
class LoggerConfig:
    LOG_TO_CONSOLE: bool = False
    LOG_TO_FILE: bool = False

    LOG_LEVEL: int = logging.INFO
    LOG_DIR = PROJECT_ROOT / "logs"


# Directory config
@dataclass(frozen=True)
class DirectoryConfig:
    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
    PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
    SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample_tickers"

    LOG_DIR = PROJECT_ROOT / "logs"

    SRC_ROOT = PROJECT_ROOT / "src"


# Create singleton instances for easy access
DEFAULT_ARGUMENTS = DefaultArguments()
GRAPH_CONFIG = GraphConfig()
LOGGER_CONFIG = LoggerConfig()
DIRECTORY_CONFIG = DirectoryConfig()

# config.py
from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Callable

import networkx as nx


# Directory config
@dataclass(frozen=True)
class DirectoryConfig:
    """ Configuration for project directories and data storage. """
    PROJECT_ROOT = Path(__file__).resolve().parent
    RAW_DATA_DIR: Path = PROJECT_ROOT / "data" / "raw"
    PROCESSED_DATA_DIR: Path = PROJECT_ROOT / "data" / "processed"
    SAMPLE_DATA_DIR: Path = PROJECT_ROOT / "data" / "sample_tickers"
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    SRC_ROOT: Path = PROJECT_ROOT / "src"

    def ensure_dirs_exist(self):
        """ Ensure all necessary directories exist, handling any errors. """
        for path in [self.RAW_DATA_DIR, self.PROCESSED_DATA_DIR, self.SAMPLE_DATA_DIR, self.LOG_DIR]:
            try:
                path.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                print(f"Error: Permission denied while creating {path}. Check folder permissions.")
            except FileExistsError:
                print(f"Warning: {path} already exists as a file, not a directory.")
            except Exception as e:
                print(f"Unexpected error creating {path}: {e}")


DIRECTORY_CONFIG = DirectoryConfig()


# Graph config
@dataclass(frozen=True)
class GraphConfig:
    """ Configuration for graph visualizations and network analysis. """
    COLOURING_MODE: str = 'community_colouring'
    NODE_SIZE: int = 8
    EDGE_OPACITY: float = 0.6

    # Graph layout positioning
    SEED: int = 42
    K: float = 0.3
    DIM: int = 3
    LAYOUT_FUNC: Callable = nx.spring_layout
    # LAYOUT_FUNC: Callable = nx.kamada_kawai_layout
    # LAYOUT_FUNC: Callable = nx.fruchterman_reingold_layout


GRAPH_CONFIG = GraphConfig()


@dataclass(frozen=True)
class DataConfig:
    """ Default parameters for stock market analysis and modeling. """
    TICKERS = None
    START_DATE: str = "2020-01-01"
    END_DATE: str = "2024-01-01"
    INTERVAL: str = "1d"
    CORRELATION_THRESHOLD: float = 0.5


DATA_CONFIG = DataConfig()


# Logger config
@dataclass(frozen=True)
class LoggerConfig:
    """ Configuration for logging across the project. """
    LOG_TO_CONSOLE: bool = False
    LOG_TO_FILE: bool = False
    LOG_LEVEL: int = logging.INFO
    LOG_FILE_NAME_FORMAT: str = "{name}_{timestamp}.log"


LOGGER_CONFIG = LoggerConfig()


@dataclass(frozen=True)
class AppConfig:
    CORRELATION_THRESHOLD_STEP = 0.01


APP_CONFIG = AppConfig()

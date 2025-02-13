# utils/logger_setup.py
import logging
from datetime import datetime
from pathlib import Path

from config import LOGGER_CONFIG, DIRECTORY_CONFIG


def setup_logger(name: str,
                 log_to_console: bool = LOGGER_CONFIG.LOG_TO_CONSOLE,
                 log_to_file: bool = LOGGER_CONFIG.LOG_TO_FILE,
                 log_level: int = LOGGER_CONFIG.LOG_LEVEL,
                 log_dir: Path = DIRECTORY_CONFIG.LOG_DIR) -> logging.Logger:
    """
    A module level logger with configurable log locations and levels across the project.

    Args:
        name (str): The name for the logger from module (usually __name__).
        log_to_console (bool): If True, a console (Stream) handler is added.
        log_to_file (bool): If True, logs are saved to the log directory.
        log_level (int): The log level to use for both file and console (if enabled).
        log_dir (Path): Filepath logs should be saved to if enabled.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent adding multiple handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Add file handler if enabled
    if log_to_file:
        log_dir.mkdir(exist_ok=True)  # Ensure log directory exists
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"{name}_{timestamp}.log"
        file_handler = logging.FileHandler(log_dir / log_filename)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Add console handler if enabled
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

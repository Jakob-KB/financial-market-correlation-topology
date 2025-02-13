# utils/logger_setup.py
import logging
from datetime import datetime
from pathlib import Path

from config import PROJECT_ROOT


def setup_logger(name: str, add_console: bool = False, log_level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger that writes all messages to a file and, if specified, to the terminal.

    Args:
        name (str): The name for the logger (usually __name__).
        add_console (bool): If True, a console (Stream) handler is added.
        log_level (int): The log level to use for both file and console (if enabled).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Ensure the logs directory exists
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    # Create a file handler that writes everything to the file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(logs_dir / f"{name}_{timestamp}.log")
    file_handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Optionally add a console handler if specified
    if add_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# src/logger.py
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from colorlog import ColoredFormatter
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

COLOR_FORMAT = (
    "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

LOG_COLORS = {
    "DEBUG":    "cyan",
    "INFO":     "green",
    "WARNING":  "yellow",
    "ERROR":    "red",
    "CRITICAL": "bold_red",
}


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = TimedRotatingFileHandler(
            os.path.join(LOG_DIR, "app.log"),
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8",
            utc=True,
            delay=True
        )
        file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        # Console handler (с цветами)
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            COLOR_FORMAT,
            datefmt=DATE_FORMAT,
            log_colors=LOG_COLORS
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
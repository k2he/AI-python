import logging
import sys

from app.config.config import settings


def setup_logging():
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    )
    logging.basicConfig(
        level=getattr(
            logging, settings.log_level.upper(), logging.INFO
        ),  # Set the desired logging level
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str):
    """Helper to get a logger named after the module."""
    return logging.getLogger(name)

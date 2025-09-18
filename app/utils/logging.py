import logging
import sys


def setup_logging():
    log_formatter = logging.Formatter("%(levelname)s: \t  %(asctime)s - %(message)s")

    # Console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(stream_handler)

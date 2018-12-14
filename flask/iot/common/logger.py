"""Logger"""
import logging
from pathlib import Path


def init_logger(logger):
    """Init logger."""
    # create file handler and set level to debug
    log_path = Path(__file__).parent.parent.parent / 'iot.log'
    fh = logging.FileHandler(log_path, encoding='UTF-8')
    fh.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')

    # add formatter to handler
    fh.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(fh)

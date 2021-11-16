import logging
import logging.config
from core.config import CONFIG


def use(name):
    return logging.getLogger(name)


def init():
    """
    Load logging configuration from global yaml configuration
    :return:
    """
    logging.config.dictConfig(CONFIG.logging.get())


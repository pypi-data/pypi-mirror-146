"""System module."""
import logging
import os
from ._version import __version__


def get_module_logger(mod_name):
    """This function generates the logger"""
    logger = logging.getLogger(mod_name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
          '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    return logger


main_logger = get_module_logger(__name__)

main_logger.debug("Module Version: %s", __version__)

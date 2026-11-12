import logging
import os

# Ensure logs directory exists if we want to write to file,
# but for now we will just do basic console logging nicely formatted.

def setup_logger():
    logger = logging.getLogger("JarvisLogger")
    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger

logger = setup_logger()

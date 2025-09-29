import logging
import os


logger = logging.getLogger(__name__)


def setup_logger(verbose_level=1, log_file=None):
    logger.handlers.clear()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # StreamHandler for logging to the console
    ch = logging.StreamHandler()
    if args == 0:
        ch.setLevel(logging.CRITICAL)
    elif verbose_level == 1:
        ch.setLevel(logging.ERROR)
    elif verbose_level == 2:
        ch.setLevel(logging.WARNING)
    elif verbose_level == 3:
        ch.setLevel(logging.DEBUG)
    
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

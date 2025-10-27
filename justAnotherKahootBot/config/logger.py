import logging
from pathlib import Path
import os
from justAnotherKahootBot.config.state import args 

log_dir = args.log_dir
verbose_level = args.verbose

logger = logging.getLogger(__name__)



def setup_logger():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # StreamHandler for logging to the console
    ch = logging.StreamHandler()
    if verbose_level == 0:
        ch.setLevel(logging.CRITICAL)
    elif verbose_level == 1:
        ch.setLevel(logging.ERROR)
    elif verbose_level == 2:
        ch.setLevel(logging.WARNING)
    elif verbose_level == 3:
        ch.setLevel(logging.DEBUG)
    
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    os.makedirs(log_dir, exist_ok=True)

    log_file = Path(os.path.join(log_dir, "logs.log"))
    log_file.touch(exist_ok=True)
    
    fh = logging.FileHandler(log_file, mode='a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    
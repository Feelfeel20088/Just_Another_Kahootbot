import logging
from pathlib import Path
import os
from justAnotherKahootBot.config.state import args 



logger = logging.getLogger(__name__)



def setup_logger(log_dir: str = None):
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # StreamHandler
    ch = logging.StreamHandler()
    if args.verbose == 0:
        ch.setLevel(logging.INFO)
        ch.addFilter(lambda record: record.levelno in (logging.INFO, logging.CRITICAL))
    elif args.verbose == 1:
        ch.setLevel(logging.INFO)
        ch.addFilter(lambda record: record.levelno in (logging.INFO, logging.ERROR, logging.CRITICAL))
    elif args.verbose == 2:
        ch.setLevel(logging.INFO)
        ch.addFilter(lambda record: record.levelno in (logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL))
    elif args.verbose == 3:
        ch.setLevel(logging.DEBUG)

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Use overridden log_dir if provided
    effective_log_dir = log_dir or args.log_dir
    os.makedirs(effective_log_dir, exist_ok=True)
    log_file = Path(os.path.join(effective_log_dir, "logs.log"))
    log_file.touch(exist_ok=True)
    
    fh = logging.FileHandler(log_file, mode='a')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
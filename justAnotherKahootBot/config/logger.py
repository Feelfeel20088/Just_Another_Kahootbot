import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# StreamHandler for logging to the console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

log_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(log_dir, 'app.log')

# FileHandler for logging to a file
fh = logging.FileHandler(log_path, mode='w')  
fh.setLevel(logging.DEBUG) 
fh.setFormatter(formatter)
logger.addHandler(fh)


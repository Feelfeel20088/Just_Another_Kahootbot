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

logdir = "/tmp/just_another_kahootbot"
log_path = os.path.join(logdir, 'app.log')

if not os.path.exists(log_path):
    os.mkdir(logdir)

# FileHandler for logging to a file
fh = logging.FileHandler(log_path, mode='w')  
fh.setLevel(logging.DEBUG) 
fh.setFormatter(formatter)
logger.addHandler(fh)


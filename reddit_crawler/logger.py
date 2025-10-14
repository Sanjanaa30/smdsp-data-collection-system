import logging
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("reddit_crawler")
logger.propagate = False
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)

logger.setLevel(numeric_level)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Console logger 
sh.setFormatter(formatter)
logger.addHandler(sh)

# Logging into files
# log_file = os.getenv("LOG_FILE", "reddit_crawler.log") 
# fh = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)  # 10MB max, 5 backups
# fh.setFormatter(formatter)
# logger.addHandler(fh)
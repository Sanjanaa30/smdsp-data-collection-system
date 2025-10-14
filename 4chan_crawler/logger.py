import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logger = logging.getLogger("4chan_crawler")
logger.propagate = False
log_level_str = os.getenv("CHAN_LOG_LEVEL", "INFO").upper()
numeric_level = getattr(logging, log_level_str, logging.INFO)

logger.setLevel(numeric_level)
sh = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log_mode = os.getenv("CHAN_LOG_MODE").upper()
if log_mode == "FILE":
    # Logging into files
    log_file = os.getenv("CHAN_LOG_FILE", "4chan_crawler.log") 
    fh = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)  # 10MB max, 5 backups
    fh.setFormatter(formatter)
    logger.addHandler(fh)
else:
    # Console logger 
    sh.setFormatter(formatter)
    logger.addHandler(sh)
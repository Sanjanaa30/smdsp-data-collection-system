import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

try:
    # Load .env file from parent directory
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
except Exception as e:
    print(f"Failed to load .env file: {e}", file=sys.stderr)

# Create logger
logger = logging.getLogger("reddit_crawler")
logger.propagate = False  # Prevent log duplication

# Set log level
try:
    log_level_str = os.getenv("REDDIT_LOG_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(numeric_level)
except Exception as e:
    print(f"Invalid log level: {e}", file=sys.stderr)
    logger.setLevel(logging.INFO)

# Define log formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Determine logging mode
try:
    log_mode = os.getenv("REDDIT_LOG_MODE", "CONSOLE").upper()
except Exception as e:
    print(f"Error reading log mode: {e}", file=sys.stderr)
    log_mode = "CONSOLE"

if log_mode == "FILE":
    try:
        log_file = os.getenv("REDDIT_LOG_FILE")
        log_file_path = Path(log_file).resolve()
        print("log_file", log_file)

        # Ensure parent directory exists
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        fh = RotatingFileHandler(log_file_path, maxBytes=10_000_000, backupCount=5)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    except Exception as e:
        print(f"Error setting up file handler: {e}", file=sys.stderr)
        # Fallback to console logging
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
else:
    try:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    except Exception as e:
        print(f"Error setting up stream handler: {e}", file=sys.stderr)

# Example usage (can be removed in actual code)
logger.debug("Logger initialized.")
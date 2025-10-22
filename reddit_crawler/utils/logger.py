import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

class Logger:

    """
    Logger is responsible for creating and configuring a logger instance
    based on environment variables.

    Environment Variables:
        - LOG_LEVEL: The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL). Default is INFO.
        - LOG_MODE: Determines the output mode ("FILE" or "STREAM"). Default is STREAM.
        - CHAN_LOG_FILE: File path for the log file if LOG_MODE is FILE. Default is '4chan_crawler.log'.

    Usage:
        >>> logger= Logger("my_logger")
        >>> logger = logger.get_logger()
        >>> logger.info("This is a log message.")
    """
    
    def __init__(self, name):
        load_dotenv()
        self.logger = self._set_config(name)

    def _set_config(self, name):
        logger = logging.getLogger(name)
        logger.propagate = False

        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        numeric_level = getattr(logging, log_level_str, logging.INFO)
        logger.setLevel(numeric_level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        log_mode = os.getenv("LOG_MODE", "STREAM").upper()

        if not logger.handlers:  # Prevent duplicate handlers
            if log_mode == "FILE":
                log_file = os.getenv("LOG_FILE", "default.log")
                log_dir = os.path.dirname(log_file)

                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)

                fh = RotatingFileHandler(log_file, maxBytes=10_000_000, backupCount=5)
                fh.setFormatter(formatter)
                logger.addHandler(fh)
            else:
                handler = logging.StreamHandler()
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        return logger

    def get_logger(self):
        return self.logger

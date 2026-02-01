import logging
import os
import time
import traceback
import functools
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Configures the root logger with console and rotating file handlers."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "app.log"

    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] - [%(funcName)s] - %(message)s"
    formatter = logging.Formatter(log_format)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Clear existing handlers if any
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # StreamHandler: Output to Console (Info level and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # RotatingFileHandler: Output to logs/app.log (Max 5MB, 3 backups)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

def get_logger(name):
    """Utility to export a logger instance."""
    return logging.getLogger(name)

def trace_execution(func):
    """Decorator to log function execution start, end, and capture exceptions."""
    logger = logging.getLogger(func.__module__)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"Starting {func_name}...")
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.debug(f"Finished {func_name} in {duration:.4f}s")
            return result
        except Exception as e:
            error_msg = f"Exception in {func_name}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            # User rule: add a debug log for every bug found
            logger.debug(f"BUG DETECTED in {func_name}: {str(e)}")
            raise e
    return wrapper

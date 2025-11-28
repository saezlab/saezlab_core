import sys
from typing import Optional
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

__all__ = [
    'DATE_FORMAT',
    'LOG_FORMAT',
    'get_logger',
    'get_timestamped_log_path',
    'setup_logging',
]

# Default format as per the requirements, adding levelname and module name for context.
LOG_FORMAT = '[%(asctime)s]  [%(levelname)s]  [%(name)s]  %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
):
    """Configures the root logger for the application with log rotation.

    This sets up handlers for console and optional file logging.
    It uses a standardized format for all log messages and rotates
    log files when they reach a specified size.

    :param level: The minimum logging level to capture (e.g., logging.INFO).
    :param log_file: Optional path to a file for log output.
    :param max_bytes: The maximum size in bytes for a log file before it is rotated.
    :param backup_count: The number of backup log files to keep.
    """
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    # Rotating file handler (if a path is provided)
    if log_file:
        # Use RotatingFileHandler for automatic log rotation.
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # The `force=True` argument removes any existing handlers
    # on the root logger, ensuring our configuration is the only one.
    logging.basicConfig(level=level, handlers=handlers, force=True)

    # Set up a hook for unhandled exceptions to be logged automatically.
    # This addresses the "Log traceback" requirement.
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger().critical(
            'Unhandled exception', exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = handle_exception


def get_timestamped_log_path(log_dir: str, app_name: str) -> str:
    """Generates a timestamped log file path.

    :param log_dir: The directory where the log file should be stored.
    :param app_name: The base name for the log file.
    :return: A string representing the full path to the log file.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d')
    return f'{log_dir}/{app_name}_{timestamp}.log'


def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance for the given name.

    This is the primary function that developers will use to get a
    pre-configured logger within their modules.
    """
    return logging.getLogger(name)

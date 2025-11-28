import os
from typing import Optional
import logging

from . import logger

__all__ = [
    'Session',
]


class Session:
    """Manages the application session, primarily for initializing the logger.
    This class ensures that logging is configured only once.
    """

    _initialized = False

    @classmethod
    def initialize(
        cls,
        log_level: str = 'INFO',
        log_path: Optional[str] = None,
        app_name: str = 'application',
    ):
        """Initializes the session by setting up the logging system.

        This method should be called once at the application's entry point.
        If `log_path` is a directory, a timestamped log file will be created within it.
        If `log_path` is a file path, it will be used directly.
        If `log_path` is None, logs will only be sent to the console.

        :param log_level: The logging level as a string (e.g., "DEBUG", "INFO").
        :param log_path: Optional path to a log file or a directory for logs.
        :param app_name: The base name for the application, used for timestamped logs.
        """
        if cls._initialized:
            # Using the logger itself to warn about re-initialization.
            logging.getLogger(__name__).warning(
                'Session.initialize() called more than once.'
            )
            return

        # Convert string level to logging constant
        level = getattr(logging, log_level.upper(), logging.INFO)

        log_file_to_use = None
        if log_path:
            # If the path is a directory, create a timestamped log file inside it.
            # Otherwise, assume it's a full file path.
            if os.path.isdir(log_path) or not os.path.splitext(log_path)[1]:
                os.makedirs(log_path, exist_ok=True)
                log_file_to_use = logger.get_timestamped_log_path(
                    log_path, app_name
                )
            else:
                # Ensure the directory for the file exists.
                log_dir = os.path.dirname(log_path)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                log_file_to_use = log_path

        logger.setup_logging(level=level, log_file=log_file_to_use)
        logging.getLogger(__name__).info(
            f'Logging session initialized with level {log_level.upper()}.'
        )

        cls._initialized = True

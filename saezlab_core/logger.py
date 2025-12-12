import os
import sys
import logging
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler

from pythonjsonlogger import jsonlogger

__all__ = [
    'get_logger',
    'setup_logging',
    'stop_async_listener',
]

_listener = None  # Global reference for QueueListener


def setup_logging(config: dict) -> None:
    """Set up logging using a DictConfig (OmegaConf) or dict.

    Supports rotation, timestamped files, console+file handlers, logger exclusion, and optional JSON logs.

    Args:
        config (dict): Logging configuration dictionary or DictConfig.
    """
    # Support both DictConfig and dict
    cfg = config if isinstance(config, dict) else dict(config)
    log_dir = cfg.get('log_dir', './log')
    app_name = cfg.get('app_name', 'saezlab_core')
    log_level = getattr(logging, cfg.get('level', 'INFO').upper(), logging.INFO)
    log_format = cfg.get(
        'format', '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    )
    # Support max_megabytes (preferred) or fallback to max_bytes for backward compatibility
    if 'max_megabytes' in cfg:
        max_bytes = int(cfg.get('max_megabytes', 10)) * 1024 * 1024
    else:
        max_bytes = cfg.get('max_bytes', 10 * 1024 * 1024)
    backup_count = cfg.get('backup_count', 5)
    timestamp = cfg.get('timestamp')
    use_json = cfg.get('json_logs', False)
    timezone = cfg.get('timezone', 'UTC')
    import queue
    from datetime import datetime

    try:
        from zoneinfo import ZoneInfo

        tzinfo = ZoneInfo(timezone)
    except ImportError:
        # For Python <3.9, fallback to UTC
        import pytz

        tzinfo = pytz.timezone(timezone) if timezone != 'UTC' else None
    if not timestamp:
        timestamp = datetime.now(tz=tzinfo).strftime('%Y-%m-%d')
    async_logging = cfg.get('async_logging', False)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{app_name}_{timestamp}.log')

    # Custom formatter to inject timezone-aware asctime
    class TZFormatter(logging.Formatter):
        def __init__(
            self,
            fmt: str | None = None,
            datefmt: str | None = None,
            tz: object = None,
        ) -> None:
            super().__init__(fmt=fmt, datefmt=datefmt)
            self.tz = tz

        def formatTime(
            self, record: logging.LogRecord, datefmt: str | None = None
        ) -> str:
            dt = datetime.fromtimestamp(record.created, tz=self.tz)
            if datefmt:
                return dt.strftime(datefmt)
            return dt.isoformat()

    if use_json:
        json_format = '%(asctime)s %(levelname)s %(name)s %(message)s'
        formatter = jsonlogger.JsonFormatter(json_format)
        formatter.formatTime = (
            lambda record, datefmt=None: TZFormatter().formatTime(
                record, datefmt
            )
        )
    else:
        formatter = TZFormatter(log_format, tz=tzinfo)
    handlers = []
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(formatter)

    global _listener
    if async_logging:
        log_queue = queue.Queue(-1)
        queue_handler = QueueHandler(log_queue)
        handlers = [queue_handler]
        _listener = QueueListener(log_queue, console_handler, file_handler)
        _listener.start()
    else:
        handlers = [console_handler, file_handler]

    logging.basicConfig(level=log_level, handlers=handlers, force=True)

    # Exclude or set log level for specified loggers
    exclude_loggers = cfg.get('exclude_loggers', []) or []
    
    for logger_name in exclude_loggers:
        logger = logging.getLogger(logger_name)
        logger.info("THis is a test message to check logger exclusion.")
        logger.setLevel(logging.WARNING)
        logger.propagate = (
            False  # Prevents messages from being passed to the root logger
        )


def stop_async_listener() -> None:
    """Stop the async QueueListener if running (flushes all logs)."""
    global _listener
    if _listener is not None:
        _listener.stop()
        _listener = None


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a given component/module.

    Usage:
        log = get_logger(__name__) or get_logger('my_component').

    Args:
        name (str): The logger name (usually __name__ or a component name).

    Returns:
        logging.Logger: The logger instance.
    """
    return logging.getLogger(name)

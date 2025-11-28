from saezlab_core import get_logger

__all__ = [
    'run_task_division',
]

log = get_logger(__name__)


def run_task_division():
    """A task that performs division and handles division by zero."""
    log.info('Starting Division Task.')
    numerator = 10
    denominator = 0  # This will cause a division by zero error

    try:
        result = numerator / denominator
        log.info(f'Division result: {result}')
        return result
    except ZeroDivisionError:
        log.exception('Division by zero encountered in Division Task.')
        return None

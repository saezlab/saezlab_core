from saezlab_core import get_logger

__all__ = [
    'run_task_a',
]

log = get_logger(__name__)


def run_task_a():
    """A dummy task that logs its progress."""
    log.info('Starting Task A.')
    log.debug('Performing some complex calculations for Task A...')
    # Simulate some work
    result = 2 + 2
    log.info(f'Task A finished with result: {result}')
    return result

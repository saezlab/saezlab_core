from saezlab_core import get_logger

__all__ = [
    'run_task_b',
]

log = get_logger(__name__)


def run_task_b():
    """Another dummy task that logs its progress and might encounter an issue."""
    log.info('Starting Task B.')
    log.warning(
        'This task is deprecated and will be removed in a future version.'
    )
    # Simulate a potential issue
    data = None
    if data is None:
        log.error('Input data for Task B is missing.')
        return None

    log.info('Task B finished.')
    return True

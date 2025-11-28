import numpy as np

from saezlab_core import (  # TODO: Every package should have this import
    Session,
    module_a,
    module_b,
    module_c,
    module_d,
    get_logger,
)

__all__ = [
    'main',
]


def main():
    """A more complex main function to demonstrate logging from multiple modules."""
    # Initialize the session once at the start.
    # The user only needs to provide the log directory and an application name.
    Session.initialize(
        log_level='ERROR', log_path='./log', app_name='saezlab_core'
    )

    # Get a logger for the main application entry point.
    log = get_logger(__name__)  # TODO: Every package should have this import

    log.info('Main application process starting.')

    # --- Run Task A ---
    log.info('Calling module A...')
    result_a = module_a.run_task_a()
    log.debug(f'Module A returned: {result_a}')

    # --- Run Task B ---
    log.info('Calling module B...')
    result_b = module_b.run_task_b()
    if result_b is None:
        log.warning('Module B indicated a problem, but we are continuing.')

    # --- Use Module C ---
    log.info('Calling module C (the silent one)...')
    result_c = module_c.utility_function()
    # Note: We log about module C from main.py, but module_c.py itself is silent.
    log.debug(f"Module C returned: '{result_c}'")

    # --- Additional Complex Operation ---
    log.info('Performing a complex operation in main...')
    array = np.array([1, 2, 3, 4, 5])
    mean_value = np.mean(array)
    log.debug(f'Computed mean of array {array}: {mean_value}')

    # --- Handle an Exception ---
    log.info('Attempting a risky operation...')
    result = module_d.run_task_division()
    if result is None:
        log.error('Risky operation failed due to an error.')

    log.info('Main application process finished.')


if __name__ == '__main__':
    main()

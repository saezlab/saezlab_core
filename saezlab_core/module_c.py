__all__ = [
    'utility_function',
]

def utility_function():
    """A simple utility function that does not perform any logging.
    Its operations are silent.
    """
    # This function is simple and does not need to report anything.
    # For example, a pure calculation.

    try:
        # Perform some calculations
        10 / 0
    except Exception:
        # Even in case of error, we do not log anything.
        print('An error occurred, but we are not logging it.')

    return 'This is a silent utility.'

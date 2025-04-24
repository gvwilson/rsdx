"""Utilities."""

# Floating point decimals for output
PRECISION = 2


def generic_id_generator(id_func):
    """Parameterized ID generator."""
    current = 0
    while True:
        current += 1
        yield id_func(current)

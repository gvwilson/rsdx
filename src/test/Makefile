# test

include ../../examples.mk

## start: initial tests
start:
	pytest test_grid_start.py

## randomizer: test passing fake 'random' function into constructor
randomizer:
	pytest test_grid_randomizer.py

## mock: test mocking random number generation
mock:
	pytest test_grid_mock.py

## parametrize: test parameterizing across classes
parametrize:
	pytest test_grid_parametrize.py

## filled: test with explicit filling
filled:
	pytest test_grid_filled.py

## coverage: test with coverage
coverage:
	coverage run -m pytest test_grid_filled.py
	coverage report -m
	coverage html

settings: _settings

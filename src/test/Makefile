include ../../examples.mk

## start: initial tests
.PHONY: start
start:
	pytest test_grid_start.py

## randomizer: test passing fake 'random' function into constructor
.PHONY: randomizer
randomizer:
	pytest test_grid_randomizer.py

## mock: test mocking random number generation
.PHONY: mock
mock:
	pytest test_grid_mock.py

## parametrize: test parameterizing across classes
.PHONY: parametrize
parametrize:
	pytest test_grid_parametrize.py

## filled: test with explicit filling
.PHONY: filled
filled:
	pytest test_grid_filled.py

## coverage: test with coverage
.PHONY: coverage
coverage:
	coverage run -m pytest test_grid_filled.py
	coverage report -m
	coverage html

.PHONY: settings
settings: _settings

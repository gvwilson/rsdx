# cleanup

include ../../examples.mk

## original: run demo of original program
original:
	@echo "original"
	python script.py 15 15 5 98765

## refactored: run demo of refactored program
refactored:
	@echo "refactored list"
	python invperc.py list 15 15 5 98765
	@echo "refactored array"
	python invperc.py array 15 15 5 98765

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

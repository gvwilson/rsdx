# mutate

include ../../examples.mk

DATA := ../../data

## lint: run linting checks on data
lint:
	python lint.py --params ${DATA}/params/assays.json --assays ${DATA}/assays --designs ${DATA}/designs

settings: _settings
	@echo "DATA:" ${DATA}

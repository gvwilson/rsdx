include ../../examples.mk

## original: run demo of original program
.PHONY: original
original:
	@echo "original"
	python script.py 15 15 5 98765

## refactored: run demo of refactored program
.PHONY: refactored
refactored:
	@echo "refactored list"
	python invperc.py list 15 15 5 98765
	@echo "refactored array"
	python invperc.py array 15 15 5 98765

.PHONY: settings
settings: _settings

# package

include ../../examples.mk

ARTEFACTS := dist docs invperc.egg-info

## build: create package
build:
	python -m build

## docs: create documentation
docs:
	pdoc --docformat google -o ./html invperc

## tidy: remove generated artefacts
tidy:
	@rm -rf ${ARTEFACTS}

settings: _settings
	@echo "ARTEFACTS:" ${ARTEFACTS}

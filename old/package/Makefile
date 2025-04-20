# package

include ../../examples.mk

ARTEFACTS := dist docs invperc.egg-info

## build: create package
build:
	bash build.sh

## docs: create documentation
docs:
	bash docs.sh

## tidy: remove generated artefacts
tidy:
	@rm -rf ${ARTEFACTS}

settings: _settings
	@echo "ARTEFACTS:" ${ARTEFACTS}

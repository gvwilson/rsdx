# By default, show available commands
.DEFAULT: commands

# Tools
JEKYLL := jekyll
PYTHON := python

# Directories.
ASSETS := assets
SRC_DIR := src
HTML_DIR := _site

# Files.
ASSETS := $(wildcard ${ASSETS}/*.*)
MARKDOWN := ${SRC_DIR}/index.md $(wildcard src/*/index.md)
EXAMPLE_DIRS := $(dir $(patsubst %/Makefile,%,$(wildcard src/*/Makefile)))

# Generated output.
HTML := $(patsubst ${SRC_DIR}/%.md,${HTML_DIR}/%.html,${MARKDOWN})

# ----------------------------------------------------------------------

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## examples: rebuild examples
.PHONY: examples
examples:
	@for d in ${EXAMPLE_DIRS}; do echo ""; echo $$d; make -C $$d; done

## --------------------

## build: rebuild the site
.PHONY: build
build:
	${JEKYLL} build

## serve: rebuild and serve the site
.PHONY: serve
serve:
	${JEKYLL} serve

## --------------------

## style: check code style
.PHONY: style
style:
	@ruff check .

## reformat: reformat unstylish code
.PHONY: reformat
reformat:
	@ruff format .

## lint: check project organization
.PHONY: lint
lint:
	@${PYTHON} bin/lint.py --config _config.yml --src src

## --------------------

## clean: tidy up
.PHONY: clean
clean:
	@rm -rf ${HTML_DIR}
	@find . -name '*~' -exec rm {} \;

## sterile: really tidy up
.PHONY: sterile
sterile: clean
	@rm -rf ${OUT_DIR}

## --------------------

## settings: show variables
.PHONY: settings
settings:
	@echo "EXAMPLE_MAKEFILES" ${EXAMPLE_MAKEFILES}
	@echo "HTML" ${HTML}
	@echo "HTML_DIR" ${HTML_DIR}
	@echo "JEKYLL" ${JEKYLL}
	@echo "MARKDOWN" ${MARKDOWN}
	@echo "SRC_DIR" ${SRC_DIR}

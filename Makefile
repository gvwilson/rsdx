# By default, show available commands
.DEFAULT: commands

# Tools
ARK := ark
PYTHON := python

# Directories.
ASSETS := assets
DATA_DIR := data
SRC_DIR := src
HTML_DIR := _site

# Files.
ASSETS := $(wildcard ${ASSETS}/*.*)
CONFIG := config.py
MARKDOWN := ${SRC_DIR}/index.md $(wildcard src/*/index.md)
EXAMPLE_DIRS := $(dir $(patsubst %/Makefile,%,$(wildcard src/*/Makefile)))
EXAMPLE_PY := $(wildcard ${SRC_DIR}/*/*.py)

# Generated output.
HTML := $(patsubst ${SRC_DIR}/%.md,${HTML_DIR}/%.html,${MARKDOWN})

# ----------------------------------------------------------------------

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## datafiles: recreate data files
.PHONY: datafiles
datafiles:
	python bin/generate_geocoded_data.py \
		--csvdir ${DATA_DIR}/survey_tidy \
		--dbfile ${DATA_DIR}/survey.db \
		--paramsdir ${DATA_DIR}/survey_params \
		--seed 12345

## examples: rebuild examples
.PHONY: examples
examples:
	@for d in ${EXAMPLE_DIRS}; do echo ""; echo $$d; make -C $$d; done

## docs: rebuild code documentation
docs: DOCS.md
DOCS.md: ${EXAMPLE_PY} bin/make_docs.py
	@python bin/make_docs.py \
		--config ${CONFIG} \
		--src ${SRC_DIR} \
		--title "Documentation" \
		--notdirs conduct docs license \
		--notfiles '*/test_*.py' \
		> $@

## --------------------

## build: rebuild the site
.PHONY: build
build: DOCS.md
	${ARK} build

## serve: rebuild and serve the site
.PHONY: serve
serve: DOCS.md
	${ARK} serve

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
	@${PYTHON} bin/lint.py --config ${CONFIG} --src src

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
	@find . -name __pycache__ -exec rm -r {} +
	@find . -name .pytest_cache -exec rm -r {} +

## --------------------

## settings: show variables
.PHONY: settings
settings:
	@echo "ARK" ${ARK}
	@echo "DATA_DIR" ${DATA_DIR}
	@echo "EXAMPLE_MAKEFILES" ${EXAMPLE_MAKEFILES}
	@echo "EXAMPLE_PY" ${EXAMPLE_PY}
	@echo "HTML" ${HTML}
	@echo "HTML_DIR" ${HTML_DIR}
	@echo "MARKDOWN" ${MARKDOWN}
	@echo "SRC_DIR" ${SRC_DIR}

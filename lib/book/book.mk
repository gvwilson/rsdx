# By default, show available commands
.DEFAULT: commands

# Tools
ARK := ark
PYTHON := python

# Directories.
ARK_BIN := lib/book/extensions
SRC_DIR := src
HTML_DIR := docs

# Files.
CONFIG := config.py
MARKDOWN := ${SRC_DIR}/index.md $(wildcard src/*/index.md)

# Generated output.
HTML := $(patsubst ${SRC_DIR}/%.md,${HTML_DIR}/%.html,${MARKDOWN})

# ----------------------------------------------------------------------

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild the site
.PHONY: build
build: ${BUILD_EXTRAS}
	@mkdir -p ${HTML_DIR}
	${ARK} build

## serve: rebuild and serve the site
.PHONY: serve
serve: ${BUILD_EXTRAS}
	@mkdir -p ${HTML_DIR}
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
lint: ${HTML}
	@${PYTHON} ${ARK_BIN}/lint.py --config ${CONFIG} --src src

## valid: run html5validator on generated files
.PHONY: valid
valid:
	@html5validator --root ${HTML_DIR} ${HTML} \
	--ignore \
	'Attribute "markdown" not allowed on element'

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

## order: show chapter order
.PHONY: order
order:
	@python ${ARK_BIN}/order.py ${CONFIG}

# book_settings: show common settings
.PHONY: book_settings
book_settings:
	@echo "ARK:" ${ARK}
	@echo "ARK_BIN:" ${ARK_BIN}
	@echo "CONFIG:" ${CONFIG}
	@echo "HTML:" ${HTML}
	@echo "HTML_DIR:" ${HTML_DIR}
	@echo "MARKDOWN:" ${MARKDOWN}
	@echo "SRC_DIR:" ${SRC_DIR}

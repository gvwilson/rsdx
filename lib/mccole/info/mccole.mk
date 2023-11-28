# By default, show available commands
.DEFAULT: commands

# Directories.
ARK_BIN := lib/mccole/bin
SRC_DIR := src
HTML_DIR := docs

# Tools
ARK := ark
BIBTEX := biber
LATEX := xelatex
PYTHON := python
CONVERT_SVG := ${ARK_BIN}/convert_svg.sh

# Files.
BIBLIOGRAPHY := info/bibliography.bib
TEX_CLASS := lib/mccole/info/krantz.cls
CONFIG := config.py
MARKDOWN := ${SRC_DIR}/index.md $(wildcard ${SRC_DIR}/*/index.md)

# Configuration.
SLUG := $(shell python ${CONFIG} --slug)
BUILD_DATE := $(shell date '+%Y-%m-%d')
STEM := $(strip ${SLUG})-${BUILD_DATE}

# Generated output.
HTML := $(patsubst ${SRC_DIR}/%.md,${HTML_DIR}/%.html,${MARKDOWN})
TEX_FILE := ${HTML_DIR}/${STEM}.tex

# ----------------------------------------------------------------------

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild the site
.PHONY: build
build:
	@mkdir -p ${HTML_DIR}
	${ARK} build

## serve: rebuild and serve the site
.PHONY: serve
serve:
	@mkdir -p ${HTML_DIR}
	${ARK} serve

## docs: rebuild code documentation
docs: DOCS.md
DOCS.md: ${ARK_BIN}/make_docs.py
	python ${ARK_BIN}/make_docs.py \
		--config ${CONFIG} \
		--src ${SRC_DIR} \
		--title "Documentation" \
		--notdirs conduct docs license \
		--notfiles '*/test_*.py' \
		> $@

## readme: rebuild README file
readme: ${ARK_BIN}/make_readme.py
	python ${ARK_BIN}/make_readme.py \
		--config ${CONFIG} \
		--links info/links.yml \
		--outfile README.md

## latex: re-create all-in-one LaTeX file
latex:
	@${PYTHON} ${ARK_BIN}/html2tex.py --config ${CONFIG} --outfile ${TEX_FILE}

## pdf: create PDF version of material
pdf: ${DOCS_PDF}
	cp ${BIBLIOGRAPHY} docs
	cp ${TEX_CLASS} docs
	cd docs && ${LATEX} ${STEM}
	cd docs && ${BIBTEX} ${STEM}
	cd docs && ${LATEX} ${STEM}
	cd docs && ${LATEX} ${STEM}

# Generated PDFs
SRC_SVG := $(wildcard ${SRC_DIR}/*/*.svg)
SRC_PDF := $(patsubst ${SRC_DIR}/%.svg,${SRC_DIR}/%.pdf,${SRC_SVG})
DOCS_PDF := $(patsubst ${SRC_DIR}/%.pdf,${HTML_DIR}/%.pdf,${SRC_PDF})

## diagrams: convert diagrams from SVG to PDF
diagrams: ${DOCS_PDF}
${SRC_DIR}/%.pdf: ${SRC_DIR}/%.svg ${CONVERT_SVG}
	${CONVERT_SVG} $< $@
${HTML_DIR}/%.pdf: ${SRC_DIR}/%.pdf
	cp $< $@

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

## bibvalid: validate bibliography
.PHONY: bibvalid
bibvalid:
	@${BIBTEX} --tool --validate-datamodel info/bibliography.bib

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
	@find . -name '*.blg' -exec rm {} \;
	@find . -name __pycache__ -exec rm -r {} +
	@find . -name .pytest_cache -exec rm -r {} +

## sterile: really tidy up
.PHONY: sterile
sterile: clean
	@rm -rf ${OUT_DIR}

## --------------------

## order: show chapter order
.PHONY: order
order:
	@python ${CONFIG} --order

# book_settings: show common settings
.PHONY: book_settings
book_settings:
	@echo "ARK:" ${ARK}
	@echo "ARK_BIN:" ${ARK_BIN}
	@echo "BUILD_DATE:" ${BUILD_DATE}
	@echo "CONFIG:" ${CONFIG}
	@echo "DOCS_PDF:" ${DOCS_PDF}
	@echo "HTML:" ${HTML}
	@echo "HTML_DIR:" ${HTML_DIR}
	@echo "LATEX:" ${LATEX}
	@echo "MARKDOWN:" ${MARKDOWN}
	@echo "SLUG:" ${SLUG}
	@echo "SRC_DIR:" ${SRC_DIR}
	@echo "SRC_PDF:" ${SRC_PDF}
	@echo "SRC_SVG:" ${SRC_SVG}
	@echo "STEM:" ${STEM}

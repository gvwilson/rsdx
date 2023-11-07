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
EXAMPLE_DIRS := $(patsubst %/Makefile,%,$(wildcard src/*/Makefile))
EXAMPLE_PY := $(wildcard ${SRC_DIR}/*/*.py)

# Generated output.
HTML := $(patsubst ${SRC_DIR}/%.md,${HTML_DIR}/%.html,${MARKDOWN})

# Parameters.
PARAMS_STEMS := params sites surveys
SITES_STEMS := COT GBY HMB YOU

# ----------------------------------------------------------------------

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## demos: re-run all demos
.PHONY: demos
demos:
	@for d in ${EXAMPLE_DIRS}; do echo ""; echo $$d; make -C $$d demo; done

## examples: rebuild examples
.PHONY: examples
examples:
	@for d in ${EXAMPLE_DIRS}; do echo ""; echo $$d; make -C $$d examples; done

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

PARAMS_FILES := $(patsubst %,${DATA_DIR}/survey_params/%.csv,${PARAMS_STEMS})
TIDY_FILES := $(patsubst %,${DATA_DIR}/survey_tidy/%.csv,${SITES_STEMS})
RAW_FILES := $(patsubst %,${DATA_DIR}/survey_raw/%.csv,${SITES_STEMS})
DB_FILE := ${DATA_DIR}/survey.db
DB_DUMP := ${DATA_DIR}/survey.sql
GENOME_FILE := ${DATA_DIR}/genomes.json
SNAILS_FILE := ${DATA_DIR}/snails.csv

## datafiles: recreate data files
.PHONY: datafiles
datafiles: ${PARAMS_FILES} ${TIDY_FILES} ${DB_DUMP} ${DB_FILE} ${RAW_FILES} ${GENOME_FILE} ${SNAILS_FILE}

${PARAMS_FILES} ${TIDY_FILES} ${DB_FILE}: bin/generate_geocoded_data.py
	@mkdir -p ${DATA_DIR}/survey_params ${DATA_DIR}/survey_tidy
	python bin/generate_geocoded_data.py \
		--csvdir ${DATA_DIR}/survey_tidy \
		--dbfile ${DATA_DIR}/survey.db \
		--paramsdir ${DATA_DIR}/survey_params \
		--seed 12345

${DB_DUMP}: ${DB_FILE}
	sqlite3 ${DATA_DIR}/survey.db .dump > ${DATA_DIR}/survey.sql

${RAW_FILES}: ${TIDY_FILES} bin/randomize_geocoded_data.py
	@mkdir -p ${DATA_DIR}/survey_raw
	python bin/randomize_geocoded_data.py \
		--tidydir ${DATA_DIR}/survey_tidy \
		--rawdir ${DATA_DIR}/survey_raw

${GENOME_FILE}: bin/generate_genomes.py
	@mkdir -p ${DATA_DIR}
	python bin/generate_genomes.py \
		--length 30 \
		--num_genomes 90 \
		--num_mutations 3 5 \
		--seed 67890 \
		--outfile $@

${SNAILS_FILE}: ${PARAMS_FILES} ${GENOME_FILE} bin/generate_snail_samples.py
	@mkdir -p ${DATA_DIR}
	python bin/generate_snail_samples.py \
		--genomes ${GENOME_FILE} \
		--site YOU \
		--paramsdir data/survey_params/ \
		--probs 0.9 0.1 \
		--seed 1738 \
		--outfile $@

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

## order: show chapter order
.PHONY: order
order:
	@python bin/show_order.py ${CONFIG}

## settings: show variables
.PHONY: settings
settings:
	@echo "ARK:" ${ARK}
	@echo "CONFIG:" ${CONFIG}
	@echo "DATA_DIR:" ${DATA_DIR}
	@echo "EXAMPLE_DIRS:" ${EXAMPLE_DIRS}
	@echo "EXAMPLE_PY:" ${EXAMPLE_PY}
	@echo "HTML:" ${HTML}
	@echo "HTML_DIR:" ${HTML_DIR}
	@echo "MARKDOWN:" ${MARKDOWN}
	@echo "SITES:" ${SITES}
	@echo "SRC_DIR:" ${SRC_DIR}

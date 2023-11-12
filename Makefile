include lib/book/book.mk

# Directories
BIN := bin
DATA_DIR := data

# Files.
EXAMPLE_DIRS := $(patsubst %/Makefile,%,$(wildcard src/*/Makefile))
EXAMPLE_PY := $(wildcard ${SRC_DIR}/*/*.py)

# ----------------------------------------------------------------------

## demos: re-run all demos
.PHONY: demos
demos:
	@for d in ${EXAMPLE_DIRS}; do echo ""; echo $$d; make -C $$d demo; done

## examples: rebuild examples
.PHONY: examples
examples:
	@for d in ${EXAMPLE_DIRS}; do echo ""; echo $$d; make -C $$d examples; done

## --------------------

PARAMS_STEMS := sites surveys
SITES_STEMS := COT GBY HMB YOU

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

${TIDY_FILES} ${DB_FILE}: bin/generate_geocoded_data.py ${PARAMS_FILES}
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
		--num_genomes 200 \
		--num_snp 3 \
		--prob_other 0.05 \
		--seed 67890 \
		--outfile $@

${SNAILS_FILE}: ${PARAMS_FILES} ${GENOME_FILE} bin/generate_snail_samples.py
	@mkdir -p ${DATA_DIR}
	python bin/generate_snail_samples.py \
		--genomes ${GENOME_FILE} \
		--site YOU \
		--paramsdir data/survey_params/ \
		--scales 1.0 0.1 \
		--seed 1738 \
		--outfile $@

## --------------------

## settings: show variables
.PHONY: settings
settings: book_settings
	@echo "--------------------"
	@echo "BIN:" ${BIN}
	@echo "DATA_DIR:" ${DATA_DIR}
	@echo "EXAMPLE_DIRS:" ${EXAMPLE_DIRS}
	@echo "EXAMPLE_PY:" ${EXAMPLE_PY}

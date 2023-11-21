include lib/mccole/info/mccole.mk

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

SURVEY_PARAMS_FILES := $(wildcard ${DATA_DIR}/survey_params/*.csv)
SURVEY_SITES_STEMS := $(shell tail -n +2 ${DATA_DIR}/survey_params/sites.csv | cut -d , -f 1)
TIDY_SURVEY_FILES := $(patsubst %,${DATA_DIR}/survey_tidy/%.csv,${SURVEY_SITES_STEMS})
MESSY_SURVEY_FILES := $(patsubst %,${DATA_DIR}/survey_raw/%.csv,${SURVEY_SITES_STEMS})
SURVEY_DB_FILE := ${DATA_DIR}/survey_db/survey.db
SURVEY_SQL_DUMP := ${DATA_DIR}/survey_db/survey.sql
SNAIL_GENOMES_FILE := ${DATA_DIR}/snails/snail_genomes.json
SNAIL_SAMPLES_FILE := ${DATA_DIR}/snails/snail_samples.csv

## datafiles: recreate data files
.PHONY: datafiles
datafiles: ${TIDY_SURVEY_FILES} ${SURVEY_SQL_DUMP} ${SURVEY_DB_FILE} ${MESSY_SURVEY_FILES} ${SNAIL_GENOMES_FILE} ${SNAIL_SAMPLES_FILE}

${TIDY_SURVEY_FILES} ${SURVEY_DB_FILE}: bin/make_tidy_pollution_samples.py ${SURVEY_PARAMS_FILES}
	@mkdir -p ${DATA_DIR}/survey_tidy ${DATA_DIR}/survey_db
	python bin/make_tidy_pollution_samples.py \
		--csvdir ${DATA_DIR}/survey_tidy \
		--dbfile ${DATA_DIR}/survey_db/survey.db \
		--paramsdir ${DATA_DIR}/survey_params \
		--seed 12345

${MESSY_SURVEY_FILES}: ${TIDY_SURVEY_FILES} bin/make_messy_pollution_samples.py
	@mkdir -p ${DATA_DIR}/survey_raw
	python bin/make_messy_pollution_samples.py \
		--tidydir ${DATA_DIR}/survey_tidy \
		--rawdir ${DATA_DIR}/survey_raw

${SURVEY_SQL_DUMP}: ${SURVEY_DB_FILE}
	sqlite3 ${DATA_DIR}/survey_db/survey.db .dump > ${DATA_DIR}/survey_db/survey.sql

${SNAIL_GENOMES_FILE}: ${SRC_DIR}/mut/make_snail_genomes.py
	@mkdir -p ${DATA_DIR}/snails
	python ${SRC_DIR}/mut/make_snail_genomes.py \
		--length 30 \
		--num_genomes 200 \
		--num_snp 3 \
		--prob_other 0.05 \
		--seed 67890 \
		--outfile $@

${SNAIL_SAMPLES_FILE}: ${SURVEY_PARAMS_FILES} ${SNAIL_GENOMES_FILE} bin/make_snail_samples.py
	@mkdir -p ${DATA_DIR}/snails
	python bin/make_snail_samples.py \
		--genomes ${SNAIL_GENOMES_FILE} \
		--site YOU \
		--paramsdir ${DATA_DIR}/survey_params/ \
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
	@echo "--------------------"
	@echo "SURVEY_PARAMS_FILES:" ${SURVEY_PARAMS_FILES}
	@echo "SURVEY_SITES_STEMS:" ${SURVEY_SITES_STEMS}
	@echo "TIDY_SURVEY_FILES:" ${TIDY_SURVEY_FILES}
	@echo "MESSY_SURVEY_FILES:" ${MESSY_SURVEY_FILES}
	@echo "SURVEY_DB_FILE:" ${SURVEY_DB_FILE}
	@echo "SURVEY_SQL_DUMP:" ${SURVEY_SQL_DUMP}
	@echo "SNAIL_GENOMES_FILE:" ${SNAIL_GENOMES_FILE}
	@echo "SNAIL_SAMPLES_FILE:" ${SNAIL_SAMPLES_FILE}

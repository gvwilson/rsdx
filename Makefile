include lib/mccole/info/mccole.mk

# Directories
BIN := bin
DATA := data

## --------------------

SURVEY_PARAMS_FILES := ${DATA}/params/sites.csv ${DATA}/params/surveys.csv
SURVEY_SITES_STEMS := $(shell tail -n +2 ${DATA}/params/sites.csv | cut -d , -f 1)
TIDY_SURVEY_FILES := $(patsubst %,${DATA}/survey_tidy/%.csv,${SURVEY_SITES_STEMS})
RAW_SURVEY_FILES := $(patsubst %,${DATA}/survey_raw/%.csv,${SURVEY_SITES_STEMS})
SURVEY_DB := ${DATA}/survey.db
ASSAY_DB := ${DATA}/assay.db
ASSAY_PARAMS := ${DATA}/params/assays.json
ASSAY_PLATES_DIR := ${DATA}/assays
ASSAY_TABLES := ${DATA}/params/assay_tables.sql

## datafiles: recreate data files
datafiles: ${TIDY_SURVEY_FILES} ${RAW_SURVEY_FILES} ${SURVEY_DB} ${ASSAY_DB}

${TIDY_SURVEY_FILES}: bin/make_tidy_samples.py ${SURVEY_PARAMS_FILES}
	@mkdir -p ${DATA}/survey_tidy
	python bin/make_tidy_samples.py \
		--paramsdir ${DATA}/params \
		--csvdir ${DATA}/survey_tidy \
		--seed 12345

${RAW_SURVEY_FILES}: bin/make_raw_samples.py ${TIDY_SURVEY_FILES}
	@mkdir -p ${DATA}/survey_raw
	python bin/make_raw_samples.py \
		--tidydir ${DATA}/survey_tidy \
		--rawdir ${DATA}/survey_raw

${SURVEY_DB}: bin/make_survey_db.py ${SURVEY_PARAMS_FILES} ${TIDY_SURVEY_FILES}
	@mkdir -p ${DATA}
	python bin/make_survey_db.py \
		--dbfile ${SURVEY_DB} \
		--paramsdir ${DATA}/params \
		--samplesdir ${DATA}/survey_tidy

${ASSAY_DB}: bin/make_assay_data.py ${ASSAY_PARAMS}
	@mkdir -p ${DATA}
	@mkdir -p ${ASSAY_PLATES_DIR}
	python bin/make_assay_data.py \
		--params ${ASSAY_PARAMS} \
		--dbfile $@ \
		--tables ${ASSAY_TABLES} \
		--platedir ${ASSAY_PLATES_DIR}

## --------------------

## settings: show variables
settings: book_settings
	@echo "--------------------"
	@echo "ASSAY_DB:" ${ASSAY_DB}
	@echo "ASSAY_PARAMS:" ${ASSAY_PARAMS}
	@echo "ASSAY_PLATES_DIR:" ${ASSAY_PLATES_DIR}
	@echo "ASSAY_TABLES:" ${ASSAY_TABLES}
	@echo "BIN:" ${BIN}
	@echo "DATA:" ${DATA}
	@echo "RAW_SURVEY_FILES:" ${RAW_SURVEY_FILES}
	@echo "SURVEY_PARAMS_FILES:" ${SURVEY_PARAMS_FILES}
	@echo "SURVEY_SITES_STEMS:" ${SURVEY_SITES_STEMS}
	@echo "TIDY_SURVEY_FILES:" ${TIDY_SURVEY_FILES}

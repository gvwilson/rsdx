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
ASSAY_PLATE_STEM := ${DATA}/assays/assay
ASSAY_PLATES := $(patsubst %,${ASSAY_PLATE_STEM}-%.csv,$(shell seq -w 0 1 99))

## datafiles: recreate data files
datafiles: ${TIDY_SURVEY_FILES} ${RAW_SURVEY_FILES} ${SURVEY_DB} ${ASSAY_PLATES}

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

${ASSAY_PLATES}: bin/make_assay_plates.py
	@mkdir -p ${DATA}/assays
	bin/make_assay_plates.py \
		--control 5 \
		--treated 8 \
		--stdev 3 \
		--num 100 \
		--seed 1789426 \
		--stem ${ASSAY_PLATE_STEM}

## --------------------

## settings: show variables
settings: book_settings
	@echo "--------------------"
	@echo "ASSAY_PLATES:" ${ASSAY_PLATES}
	@echo "BIN:" ${BIN}
	@echo "DATA:" ${DATA}
	@echo "RAW_SURVEY_FILES:" ${RAW_SURVEY_FILES}
	@echo "SURVEY_PARAMS_FILES:" ${SURVEY_PARAMS_FILES}
	@echo "SURVEY_SITES_STEMS:" ${SURVEY_SITES_STEMS}
	@echo "TIDY_SURVEY_FILES:" ${TIDY_SURVEY_FILES}

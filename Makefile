include lib/mccole/mccole.mk

# Directories
BIN := bin
DATA := data

## --------------------

## release: make a release
.PHONY: release
ifeq ($(origin RSDX_RELEASE),undefined)
release:
	@echo "RSDX_RELEASE not defined"
else
release:
	rm -rf docs ${RSDX_RELEASE}
	make build
	cp -r docs ${RSDX_RELEASE}
	find ${RSDX_RELEASE} \( -name .DS_Store -or -name '*.pdf' -or -name '*.aux' -or -name '*.bbl' -or -name '*.bcf' -or -name '*.bib' -or -name '*.blg' -or -name '*.cls' -or -name '*.idx' -or -name '*.ilg' -or -name '*.ind' -or -name '*.log' -or -name '*.tex' -or -name '*.toc' \) -exec rm {} +
	cd ${RSDX_RELEASE} && zip -q -r ${SLUG}-examples.zip . -i '*.json' '*.out' '*.py' '*.sh' '*.txt' '*.yml'
endif

## --------------------

SURVEY_PARAMS_FILES := ${DATA}/params/sites.csv ${DATA}/params/surveys.csv
SURVEY_SITES_STEMS := $(shell tail -n +2 ${DATA}/params/sites.csv | cut -d , -f 1)
TIDY_SURVEY_FILES := $(patsubst %,${DATA}/survey_tidy/%.csv,${SURVEY_SITES_STEMS})
RAW_SURVEY_FILES := $(patsubst %,${DATA}/survey_raw/%.csv,${SURVEY_SITES_STEMS})
SURVEY_DB := ${DATA}/survey.db
ASSAY_DB := ${DATA}/assays.db
ASSAY_PARAMS := ${DATA}/params/assays.json
ASSAY_DESIGNS_DIR := ${DATA}/designs
ASSAY_RESULTS_DIR := ${DATA}/assays
ASSAY_TABLES := ${DATA}/params/assay_tables.sql
STAFF_INDEX := ${DATA}/params/index.html
ASSAY_STAFF_DIR := ${DATA}/staff
STAFF_TEMPLATE := ${DATA}/params/staff.html
SNAIL_BIB_DIR := ${DATA}/bib

## datafiles: recreate data files
datafiles: ${TIDY_SURVEY_FILES} ${RAW_SURVEY_FILES} ${SURVEY_DB} ${ASSAY_DB}

## tidy_survey_files: tidy versions of snail survey files
tidy_survey_files: ${TIDY_SURVEY_FILES}
${TIDY_SURVEY_FILES}: bin/tidy_samples.py ${SURVEY_PARAMS_FILES}
	@mkdir -p ${DATA}/survey_tidy
	python bin/tidy_samples.py \
		--paramsdir ${DATA}/params \
		--csvdir ${DATA}/survey_tidy \
		--seed 12345

## raw_survey_files: reverse-engineered raw snail survey files
raw_survey_files: ${RAW_SURVEY_FILES}
${RAW_SURVEY_FILES}: bin/raw_samples.py ${TIDY_SURVEY_FILES}
	@mkdir -p ${DATA}/survey_raw
	python bin/raw_samples.py \
		--tidydir ${DATA}/survey_tidy \
		--rawdir ${DATA}/survey_raw

## survey_db: SQLite survey database
survey_db: ${SURVEY_DB}
${SURVEY_DB}: bin/survey_db.py ${SURVEY_PARAMS_FILES} ${TIDY_SURVEY_FILES}
	@mkdir -p ${DATA}
	python bin/survey_db.py \
		--dbfile ${SURVEY_DB} \
		--paramsdir ${DATA}/params \
		--samplesdir ${DATA}/survey_tidy

## assay_db: genomic assay database
assay_db: ${ASSAY_DB}
${ASSAY_DB}: bin/assay_data.py bin/assay_plates.py ${ASSAY_PARAMS}
	@mkdir -p ${DATA}
	@mkdir -p ${ASSAY_DESIGNS_DIR}
	@mkdir -p ${ASSAY_RESULTS_DIR}
	python bin/assay_data.py \
		--dbfile $@ \
		--params ${ASSAY_PARAMS} \
		--tables ${ASSAY_TABLES}
	python bin/assay_plates.py \
		--dbfile $@ \
		--params ${ASSAY_PARAMS} \
		--designs ${ASSAY_DESIGNS_DIR} \
		--results ${ASSAY_RESULTS_DIR}

## staff_pages: HTML pages for genomics staff
.PHONY: staff_pages
staff_pages:
	python bin/assay_staff.py \
		--dbfile ${ASSAY_DB} \
		--index ${STAFF_INDEX} \
		--pagedir ${ASSAY_STAFF_DIR} \
		--params ${ASSAY_PARAMS} \
		--seed 7149238 \
		--staff ${STAFF_TEMPLATE}

## staff_server: server HTML pages for genomics staff
.PHONY: staff_server
staff_server:
	python -m http.server -d ${ASSAY_STAFF_DIR} 8000


## snail_bib: create snail bibliography
.PHONY: snail_bib
snail_bib:
	@mkdir -p ${SNAIL_BIB_DIR}
	python bin/fetch_bib_data.py --outdir ${SNAIL_BIB_DIR}

## --------------------

## settings: show variables
settings: book_settings
	@echo "--------------------"
	@echo "ASSAY_DB:" ${ASSAY_DB}
	@echo "ASSAY_PARAMS:" ${ASSAY_PARAMS}
	@echo "ASSAY_RESULTS_DIR:" ${ASSAY_RESULTS_DIR}
	@echo "ASSAY_TABLES:" ${ASSAY_TABLES}
	@echo "BIN:" ${BIN}
	@echo "DATA:" ${DATA}
	@echo "RAW_SURVEY_FILES:" ${RAW_SURVEY_FILES}
	@echo "SURVEY_PARAMS_FILES:" ${SURVEY_PARAMS_FILES}
	@echo "SURVEY_SITES_STEMS:" ${SURVEY_SITES_STEMS}
	@echo "TIDY_SURVEY_FILES:" ${TIDY_SURVEY_FILES}

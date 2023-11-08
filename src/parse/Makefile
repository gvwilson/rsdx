TARGETS :=

include ../../examples.mk

DATA_DIR := ../../data
RAW_FILES := $(wildcard ${DATA_DIR}/survey_raw/*.csv)
TIDY_FILES := $(patsubst ${DATA_DIR}/survey_raw/%.csv,${DATA_DIR}/survey_tidy/%.csv,${RAW_FILES})

## demo: run demo of program
.PHONY: demo
demo:
	python parse.py --infile ${DATA_DIR}/survey_raw/COT.csv

## tidy: re-make tidied data
tidy: ${TIDY_FILES}

## settings: show settings
.PHONY: settings
settings:
	@echo "DATA_DIR:" ${DATA_DIR}
	@echo "RAW_FILES:" ${RAW_FILES}
	@echo "TIDY_FILES:" ${TIDY_FILES}

# Rule to make tidy CSV from raw CSV using parse.py
${DATA_DIR}/survey_tidy/%.csv: ${DATA_DIR}/survey_raw/%.csv parse.py
	@mkdir -p $$(dirname $@)
	python parse.py --infile $< --outfile $@

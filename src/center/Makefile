TARGETS :=

include ../../examples.mk

DATA_DIR := ../../data
CSV_DIR := ${DATA_DIR}/survey_tidy
DB_FILE := ${DATA_DIR}/survey.db

## demo: run demo of program
.PHONY: demo
demo:
	python display.py --csvdir ${CSV_DIR} --dbfile ${DB_FILE} --figdir . --methods csv pandas sql

## settings: show settings
.PHONY: settings
settings:
	@echo "CSV_DIR:" ${CSV_DIR}
	@echo "DATA_DIR:" ${DATA_DIR}
	@echo "DB_FILE:" ${DB_FILE}

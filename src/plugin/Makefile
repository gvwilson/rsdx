include ../../examples.mk

TIDY_DIR := ${DATA}/survey_tidy
SURVEY_DB := ${DATA}/survey.db

## display: display plots
.PHONY: display
display:
	python display.py --plugins plugins.json

## settings: show settings
.PHONY: settings
settings: examples_settings
	@echo "TIDY_DIR:" ${TIDY_DIR}
	@echo "SURVEY_DB:" ${SURVEY_DB}

# parse

include ../../examples.mk

STEMS := $(patsubst ${DATA}/survey_raw/%.csv,%,$(wildcard ${DATA}/survey_raw/*.csv))

## test: test parsing
test:
	@for stem in ${STEMS}; do echo $${stem}; make STEM=$${stem} _diff; done

_diff:
	@python parse.py --infile ${DATA}/survey_raw/${STEM}.csv | diff - ${DATA}/survey_tidy/${STEM}.csv

settings: _settings
	@echo "STEMS:" ${STEMS}

## naive: try running naive parser
naive:
	@for stem in ${STEMS}; do echo $${stem}; make STEM=$${stem} _naive; done

_naive:
	@python naive.py ${DATA}/survey_raw/${STEM}.csv

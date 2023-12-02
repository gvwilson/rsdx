include ../../examples.mk

STEMS := $(patsubst ${DATA}/survey_raw/%.csv,%,$(wildcard ${DATA}/survey_raw/*.csv))

## test: test parsing
.PHONY: test
test:
	@for stem in ${STEMS}; do echo $${stem}; make STEM=$${stem} _diff; done

.PHONY: diff
_diff:
	@python parse.py --infile ${DATA}/survey_raw/${STEM}.csv | diff - ${DATA}/survey_tidy/${STEM}.csv

.PHONY: settings
settings: _settings
	@echo "STEMS:" ${STEMS}

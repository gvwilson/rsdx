include ../../examples.mk

STEMS := $(patsubst ${DATA}/survey_raw/%.csv,%,$(wildcard ${DATA}/survey_raw/*.csv))

.PHONY: test
test:
	@for stem in ${STEMS}; do echo $${stem}; make STEM=$${stem} diff; done

.PHONY: diff
diff:
	@python parse.py --infile ${DATA}/survey_raw/${STEM}.csv | diff - ${DATA}/survey_tidy/${STEM}.csv

.PHONY: settings
settings: examples_settings
	@echo "STEMS:" ${STEMS}

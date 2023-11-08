TARGETS :=

include ../../examples.mk

DVC_REMOTE := /tmp/rsdx_remote

## demo: run demo of program
.PHONY: demo
demo:
	rm -rf ${DVC_REMOTE}
	mkdir -p ${DVC_REMOTE}
	dvc remote add -f -d datastore ${DVC_REMOTE}
	python flow.py run --sizes '[501]' --depth 10 --reps 100 --seed 987456 --verbose true
	python flow.py run --sizes '[501]' --depth 100 --reps 100 --seed 1729383 --verbose true
	dvc add *.csv
	dvc push
	python find_matching_files.py 2 *.csv /tmp/rsdx_remote/files/md5/*/*
	rm *.csv
	dvc remote remove datastore

## settings: show settings
.PHONY: settings
settings:
	@echo "DATA_DIR:" ${DATA_DIR}
	@echo "RAW_FILES:" ${RAW_FILES}
	@echo "ROOT:" ${ROOT}
	@echo "TIDY_FILES:" ${TIDY_FILES}

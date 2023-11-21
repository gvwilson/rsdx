TARGETS :=

include ../../examples.mk

DVC_REMOTE := /tmp/rsdx_remote

## demo: run demo of program
.PHONY: demo
demo:
	python flow.py run --sizes '[11, 13]' --depth 5 --reps 10 --seed 33819 --save true

## example: run demo of program
.PHONY: example
example:
	rm -rf ${DVC_REMOTE} ./results
	mkdir -p ${DVC_REMOTE} ./results
	dvc remote add -f -d datastore ${DVC_REMOTE}
	python flow.py run --seed 12345
	dvc add results
	dvc push
	python find_matching_files.py 2 results/*.csv /tmp/rsdx_remote/files/md5/*/*
	rm -rf results
	dvc remote remove datastore

## measure: measure properties of invasion percolation output
.PHONY: measure
measure:
	python measure.py --densities densities.svg --filenames results/*.csv
	python measure.py --densities densities.pdf --filenames results/*.csv

## settings: show settings
.PHONY: settings
settings:
	@echo "DVC_REMOTE:" ${DVC_REMOTE}
	@echo "ROOT:" ${ROOT}

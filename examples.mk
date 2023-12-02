# Get the path to this file from wherever it is included.
# See https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
ROOT:=$(realpath $(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

# Data directory.
DATA := ${ROOT}/data

## ---: ---

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'


## clean: clean up files
.PHONY: clean
clean:
	@rm -rf __pycache__ .coverage .pytest_cache *~

.PHONY: examples_settings
examples_settings:
	@echo "DATA:" ${DATA}
	@echo "ROOT:" ${ROOT}
	@echo "---"

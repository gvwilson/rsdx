# Common code to regenerate examples.

# By default, show available commands (by finding '##' comments).
.DEFAULT: commands

# Get the absolute path to this file from wherever it is included.
# See https://stackoverflow.com/questions/18136918/how-to-get-current-relative-directory-of-your-makefile
ROOT := $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

## --------------------

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

# The including file must define a variable TARGETS with the names of everything
# to be created.
examples: ${TARGETS}

## targets: Show the targets defined by the including file.
targets:
	@echo "TARGETS:" ${TARGETS}

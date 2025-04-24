include common.mk

all: commands

DATA=data
PARAMS=${DATA}/params.json
PYTHON=uv run python
PYTHON_M=${PYTHON} -m
MCCOLE=mccole
SNAILZ=snailz
DB=temp.db

## build: build HTML
build:
	${MCCOLE} build
	@touch docs/.nojekyll

## data: re-create snailz parameters and datasets
.PHONY: data
data:
	@rm -rf ${DATA} ${DB}
	@mkdir -p ${DATA}
	${SNAILZ} params --output ${PARAMS}
	${SNAILZ} data --params ${PARAMS} --output ${DATA}
	${PYTHON} 07_db/make_db.py --source ${DATA} --db ${DB}

## format: reformat code
format:
	@uv run ruff format --exclude docs --exclude old .

## lint: check code and project
lint:
	@${PYTHON_M} ruff check --exclude docs --exclude old .
	@${MCCOLE} lint
	@html5validator --root docs --blacklist templates \
	&& echo "HTML checks passed."

## serve: serve generated HTML
serve:
	@${PYTHON_M} http.server -d docs 8000

## stats: basic site statistics
stats:
	@${MCCOLE} stats

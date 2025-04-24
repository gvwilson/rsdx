include common.mk

all: commands

DATA=data
PYTHON=uv run python
PYTHON_M=${PYTHON} -m
MCCOLE=mccole
DB=98_viewer/temp.db

## build: build HTML
build:
	${MCCOLE} build
	@touch docs/.nojekyll

## data: re-create snailz parameters and datasets
.PHONY: data
data:
	@rm -rf ${DATA} ${DB}
	@mkdir -p ${DATA}
	${PYTHON} 06_scenario/scenario.py ${DATA}
	${PYTHON} 97_db/make_db.py --source ${DATA} --db ${DB}

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

## viewer: run the viewer app
viewer:
	${PYTHON} 98_viewer/app.py --db ${DB}

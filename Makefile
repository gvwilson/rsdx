include common.mk

all: commands

## datasets: re-create snailz parameters and datasets
datasets:
	snailz params --outdir params
	snailz everything --paramsdir params --datadir data

## lint: check code and project
lint:
	@ruff check --exclude docs .
	@mccole lint
	@html5validator --root docs --blacklist templates \
	&& echo "HTML checks passed."

## render: convert to HTML
render:
	mccole render
	@touch docs/.nojekyll

## serve: serve generated HTML
serve:
	@python -m http.server -d docs 8000

## stats: basic site statistics
stats:
	@mccole stats

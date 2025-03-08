include common.mk

all: commands

## build: build HTML
build:
	mccole build
	@touch docs/.nojekyll

## datasets: re-create snailz parameters and datasets
datasets:
	snailz params --outdir params
	snailz everything --paramsdir params --datadir data

## lint: check code and project
lint:
	@ruff check --exclude docs --exclude lib .
	@mccole lint
	@html5validator --root docs --blacklist templates \
	&& echo "HTML checks passed."

## refresh: refresh all file inclusions
refresh:
	mccole refresh --files *_*/index.md

## serve: serve generated HTML
serve:
	@python -m http.server -d docs 8000

## stats: basic site statistics
stats:
	@mccole stats

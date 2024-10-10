# mutate

include ../../examples.mk

ASSAY_DB = ${DATA}/assays.db

## create: make empty LIMS database
create:
	python create_db.py --sqlite ${ASSAY_DB} --tinydb lims.json

## lint: run linting checks on data
lint:
	@bash lint.sh

## listing: try listing for one user
listing:
	@bash listing.sh

## upload: try uploading a single valid file
upload:
	@bash upload.sh

## invalid_user: try uploading a single valid file with invalid user
invalid_user:
	@bash invalid_user.sh

settings: _settings

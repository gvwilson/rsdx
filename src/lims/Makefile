# mutate

include ../../examples.mk

ASSAY_DB = ${DATA}/assays.db
ASSAY_PARAMS = assays.json
LIMS_DB = lims.json
TEST_STEM = fff9b2d6
TEST_USER = f.buch

## create: make empty LIMS database
create:
	python create_db.py --sqlite ${ASSAY_DB} --tinydb ${LIMS_DB}

## lint: run linting checks on data
lint:
	python lint.py --params ${ASSAY_PARAMS} --assays ${DATA}/assays --designs ${DATA}/designs

## listing: try listing for one user
listing:
	python lims.py listing \
		--db ${LIMS_DB} \
		--user ${TEST_USER} \
		--subject ${TEST_USER}

## upload: try uploading a single valid file
upload:
	python lims.py upload \
		--db ${LIMS_DB} \
		--assay ${DATA}/assays/${TEST_STEM}.csv \
		--design ${DATA}/designs/${TEST_STEM}.csv \
		--params ${ASSAY_PARAMS} \
		--user ${TEST_USER}

## invalid_user: try uploading a single valid file with invalid user
invalid_user:
	python lims.py upload \
		--db ${LIMS_DB} \
		--assay ${DATA}/assays/${TEST_STEM}.csv \
		--design ${DATA}/designs/${TEST_STEM}.csv \
		--params ${ASSAY_PARAMS} \
		--user invalid

settings: _settings

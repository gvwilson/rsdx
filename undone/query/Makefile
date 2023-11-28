DB_FILE := lab.db
PLATES_DIR := ./plates

all:
	@rm -rf ${DB_FILE} ${PLATES_DIR}
	mkdir -p ${PLATES_DIR}
	python fill_tables.py --dbfile ${DB_FILE} --tables create_tables.sql --staff 7 --experiments 50 --seed 19473
	python make_raw_files.py --dbfile ${DB_FILE} --seed 12345 --outdir ${PLATES_DIR}

# mutate

include ../../examples.mk

LOCAL := ./data
GENOMES := ${LOCAL}/genomes.json
SAMPLES := ${LOCAL}/samples.csv

## generate: generate snail genomes and sample data
generate: ${SAMPLES}

${SAMPLES}: ${GENOMES}
	@mkdir -p ${LOCAL}
	python synthesize_samples.py --genomes ${GENOMES} --mutant 10.0 --normal 1.0 --outfile $@ --paramsdir . --site COW --seed 1791128

${GENOMES}:
	@mkdir -p ${LOCAL}
	python synthesize_genomes.py --outfile $@ --length 40 --num_genomes 100 --num_snp 5 --prob_other 0.01 --seed 102938

## analyze: analyze genome data
analyze: ${SAMPLES}
	python analyze.py --infile ${SAMPLES} --save

## tidy: remove generated data
tidy:
	@rm -rf ${LOCAL}

settings: _settings
	@echo "LOCAL:" ${LOCAL}
	@echo "GENOMES:" ${GENOMES}
	@echo "SAMPLES:" ${SAMPLES}

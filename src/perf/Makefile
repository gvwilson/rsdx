include ../../examples.mk

## single: run single sweep
.PHONY: single
single:
	python invperc_single.py params_single.json show

## small: run small sweep
.PHONY: small
small:
	python invperc_sweep.py params_small.json

## full: run full sweep
.PHONY: full
full:
	python invperc_sweep.py params_full.json

## profile: run with profiling
.PHONY: profile
profile:
	python run_profile.py > profile.txt

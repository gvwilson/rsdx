# lazy

include ../../examples.mk

## single: run single sweep
single:
	python invperc_single.py params_single.json show

## small: run small sweep
small:
	python invperc_sweep.py params_small.json

## full: run full sweep
full:
	python invperc_sweep.py params_full.json

## profile: run with profiling
profile:
	python run_profile.py > profile.txt

settings: _settings

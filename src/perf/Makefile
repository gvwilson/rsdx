# perf

include ../../examples.mk

## single: run single sweep
single:
	python invperc_single.py single.json show

## small: run small sweep
small:
	python invperc_sweep.py small.json

## full: run full sweep
full:
	python invperc_sweep.py full.json

## profile: run with profiling
profile:
	python run_profile.py > profile.txt
	head -n 10 profile.txt > profile_head.txt
	echo "…more lines…" >> profile_head.txt

settings: _settings

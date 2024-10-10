# perf

include ../../examples.mk

## single: run single sweep
single:
	python invperc_single.py single_list.json show
	python invperc_single.py single_lazy.json show

## small: run small sweep
small:
	python invperc_sweep.py small_list_array.json
	python invperc_sweep.py small_lazy_list_array.json

## full: run full sweep
full:
	python invperc_sweep.py full_list_array.json
	python invperc_sweep.py full_lazy_list_array.json

## profile: run with profiling
profile:
	python run_profile_list.py > profile_list.txt
	head -n 10 profile_list.txt > profile_list_head.txt
	echo "…more lines…" >> profile_list_head.txt
	python run_profile_lazy.py > profile_lazy.txt
	head -n 10 profile_lazy.txt > profile_lazy_head.txt
	echo "…more lines…" >> profile_lazy_head.txt

settings: _settings

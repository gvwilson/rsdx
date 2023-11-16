TARGETS :=

include ../../examples.mk

## demo: run demo of program
.PHONY: demo
demo:
	python walk.py --maxsteps 60 --radius 100.0 --stepsize 1.0 --reps 20000 --seed 41728 --outfile temp.csv
	python analyze.py --infile temp.csv --nbins 50
	@rm -f temp.csv

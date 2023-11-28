TARGETS :=

include ../../examples.mk

## demo: run demo of program
.PHONY: demo
demo:
	python flow.py run --sizes '[15, 35, 55, 75, 95, 105]' --depth 10 --reps 10 --seed 12345 --save true
	python analysis.py --infile invperc_15+35+55+75+95+105_10_12345.csv --outfile invperc_15+35+55+75+95+105_10_12345.svg
	python analysis.py --infile invperc_15+35+55+75+95+105_10_12345.csv --outfile invperc_15+35+55+75+95+105_10_12345.pdf

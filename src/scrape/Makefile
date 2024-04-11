# scrape

include ../../examples.mk

all: \
    find.out \
    medium.out \
    small.out

find.out: find_in_page.py medium.html find.sh
	@bash find.sh > $@

medium.out: parse_page.py medium.html medium.sh
	@bash medium.sh > $@

small.out: parse_page.py small.html small.sh
	@bash small.sh > $@

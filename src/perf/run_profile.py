import cProfile
import sys

from invperc_single import main

sys.argv = ["invperc_single.py", "params_profile.json"]
cProfile.run("main()", sort="tottime")
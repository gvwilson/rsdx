import cProfile
import sys

from invperc_single import main  # noqa: F401

# [main]
sys.argv = ["invperc_single.py", "profile_list.json"]
cProfile.run("main()", sort="tottime")
# [/main]

"""Regular expressions."""

import re

# Bibliography keys.
BIB_KEY = re.compile(r"^@.+?\{(.*?),", re.MULTILINE)

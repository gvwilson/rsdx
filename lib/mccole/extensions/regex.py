"""Regular expressions."""

import re

# Level-1 Markdown heading.
FIRST_H1 = re.compile(r"^#\s+.+$", re.MULTILINE)

# Match a reference to a footer link or a URL ref in an index entry.
MARKDOWN_FOOTER_LINK = re.compile(r"\[.*?\]\[(.+?)\]", re.MULTILINE)

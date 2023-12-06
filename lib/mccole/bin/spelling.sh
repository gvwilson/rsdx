#!/usr/bin/env bash

cat $(find docs -name '*.html') \
| sed \
  -e 's/&middot;//g' \
  -e "s/&lsquo;/'/g" \
  -e "s/&rsquo;/'/g" \
  -e 's/&ldquo;/"/g' \
  -e 's/&rdquo;/"/g' \
  -e 's/&lArr;//g' \
  -e 's/&rArr;//g' \
  -e 's/&nbsp;/ /g' \
  -e 's/&amp;//g' \
  -e 's/&quot;/"/g' \
  -e 's/&ndash;//g' \
  -e 's/&gt;/ /g' \
  -e 's/&lt;/ /g' \
| aspell -H --encoding=UTF-8 -l en_US list \
| sort \
| uniq

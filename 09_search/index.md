---
title: "Search"
tagline: "Build a simple search engine for bibliography abstracts."
abstract: >
    Information is only useful if it can be found,
    and how we search determines what we find.
    This lesson shows how to build a simple search engine
    using a technique called term frequency-inverse document frequency
    or [TF-IDF][tf_idf].
syllabus:
-   Create a table of term occurrences and calculate TF-IDF scores to support search.
-   Caching the lookup index rather than recalculating it on the fly.
-   Handling different character sets.
-   How the way we clean our data determines the results we get.
---

-   Time to do our literature survey
-   Want to search the abstracts of over 2000 papers
-   Use [%g tf_idf "term frequency - inverse document frequency" %] (TF-IDF)
    -   Term frequency: frequency of each word in each document
    -   Document frequency: proportion of documents in which a word appears
    -   Inverse document frequency: one over that (i.e., how specific the word is)

## Fetching Data {: #search-fetch}

-   [OpenAlex][open_alex] indexes over 250 million scholarly works
-   [PyAlex][pyalex] provides a Python interface
-   Copy, paste, and tweak example

[%inc fetch_bib_data.py pattern=func:main %]

-   Additional definitions

[%inc fetch_bib_data.py mark=const %]
[%inc fetch_bib_data.py pattern=func:parse_args %]

-   Produces 2192 JSON files

[%inc W962796421.json %]

## Building Index

-   Usual main driver

[%inc make_index.py pattern=func:main %]

-   Reading abstracts from JSON is the simple part

[%inc make_index.py pattern=func:read_abstracts %]

-   Getting words is a bit of a hack
    -   For now, remove punctuation and hope for the best

[%inc make_index.py pattern=func:get_words %]

-   Calculate term frequency

[%inc make_index.py pattern=func:calculate_tf %]

-   Calculate inverse document frequency

[%inc make_index.py pattern=func:calculate_idf %]

-   Combine values

[%inc make_index.py pattern=func:calculate_tf_idf %]

-   And save as CSV

[%inc make_index.py pattern=func:save %]

-   258,000 distinct terms (!)
    -   Of which several thousand contain non-Latin characters
-   17 documents contain the word "search"
-   Of these, W2026888704.json has the highest score

[%inc tf_idf_search.csv %]

-   Upon inspection, that abstract includes phrases like "Search Dropdown Menu toolbar search search input",
    which are probably a result of inaccurate web scraping
-   The good news is,
    TF-IDF is exactly the sort of thing we know how to write unit tests for

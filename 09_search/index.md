# Search

-   Time to do our literature survey
-   Want to search the abstracts of over 2000 papers
-   Use [term frequency-inverse document frequency](g:tf_idf) (TF-IDF)
    -   Term frequency: frequency of each word in each document
    -   Document frequency: proportion of documents in which a word appears
    -   Inverse document frequency: one over that (i.e., how specific the word is)

## Fetching Data {: #search-fetch}

-   [OpenAlex][open_alex] indexes over 250 million scholarly works
-   [PyAlex][pyalex] provides a Python interface
-   Copy, paste, and tweak example

```{data-file="fetch_bib_data.py:main"}
def main():
    """Main driver."""
    args = parse_args()
    if args.email:
        pyalex.config.email = args.email
    pager = (
        Works()
        .filter(concepts={"wikidata": args.concept})
        .paginate(method="page", per_page=200)
    )
    counter = 0
    for page in pager:
        for work in page:
            counter += 1
            if args.verbose:
                print(counter)
            ident = work["id"].split("/")[-1]
            data = {
                "doi": work["doi"],
                "year": work["publication_year"],
                "abstract": work["abstract"],
            }
            if all(data.values()):
                Path(args.outdir, f"{ident}.json").write_text(
                    json.dumps(data, ensure_ascii=False)
                )
```

-   Additional definitions

```{data-file="fetch_bib_data.py:const"}
WIKIDATA_LAND_SNAIL = "https://www.wikidata.org/wiki/Q6484264"
```
```{data-file="fetch_bib_data.py:parse_args"}
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--concept", type=str, default=WIKIDATA_LAND_SNAIL, help="Wikidata concept URL"
    )
    parser.add_argument("--email", type=str, default=None, help="user email address")
    parser.add_argument("--outdir", type=str, required=True, help="output directory")
    parser.add_argument(
        "--verbose", action="store_true", default=False, help="report progress"
    )
    return parser.parse_args()
```

-   Produces 2192 JSON files

```{data-file="W962796421.json"}
{
    "doi": "https://doi.org/10.1007/978-94-009-0343-2_40",
    "year": 1996,
    "abstract": "Helicid snails are suitable organisms for research…"
}
```

## Building Index

-   Usual main driver

```{data-file="make_index.py:main"}
def main():
    """Main driver."""
    args = parse_args()
    abstracts = read_abstracts(args.bibdir)
    words_in_file = {
        filename: get_words(abstract) for filename, abstract in abstracts.items()
    }
    term_freq = calculate_tf(words_in_file)
    inverse_doc_freq = calculate_idf(words_in_file)
    tf_idf = calculate_tf_idf(term_freq, inverse_doc_freq)
    save(args.outfile, tf_idf)
```

-   Reading abstracts from JSON is the simple part

```{data-file="make_index.py:read_abstracts"}
def read_abstracts(bibdir):
    """Extract abstracts from bibliography entries."""
    result = {}
    for filename in Path(bibdir).iterdir():
        data = json.loads(Path(filename).read_text())
        result[filename.name] = data["abstract"]
    return result
```

-   Getting words is a bit of a hack
    -   For now, remove punctuation and hope for the best

```{data-file="make_index.py:get_words"}
def get_words(text):
    """Get words from text, stripping basic punctuation."""
    words = text.split()
    for char in ",.'\"()%‰!?$‘’&~–—±·":
        words = [w.strip(char) for w in words]
    return [w for w in words if w]
```

-   Calculate term frequency

```{data-file="make_index.py:calculate_tf"}
def calculate_tf(words_in_file):
    """Calculate term frequency of each word per document."""
    result = {}
    for filename, wordlist in words_in_file.items():
        total_words = len(wordlist)
        counts = Counter(wordlist)
        for w in wordlist:
            result[(filename, w)] = counts[w] / total_words
    return result
```

-   Calculate inverse document frequency

```{data-file="make_index.py:calculate_idf"}
def calculate_idf(words_in_file):
    """Calculate inverse document frequency of each word."""
    num_docs = len(words_in_file)
    word_sets = [set(words) for words in words_in_file.values()]
    result = {}
    for word in set().union(*word_sets):
        result[word] = log(num_docs / sum(word in per_doc for per_doc in word_sets))
    return result
```

-   Combine values

```{data-file="make_index.py:calculate_tf_idf"}
def calculate_tf_idf(term_freq, inverse_doc_freq):
    """Calculate overall score for each term in each document."""
    result = defaultdict(dict)
    for (filename, word), tf in term_freq.items():
        result[word][filename] = tf * inverse_doc_freq[word]
    return result
```

-   And save as CSV

```{data-file="make_index.py:save"}
def save(outfile, tf_idf):
    """Save results as CSV."""
    outfile = sys.stdout if outfile is None else open(outfile, "w")
    writer = csv.writer(outfile)
    writer.writerow(("word", "doc", "score"))
    for word in sorted(tf_idf):
        for filename, score in sorted(tf_idf[word].items()):
            writer.writerow((word, filename, score))
    outfile.close()
```

-   258,000 distinct terms (!)
    -   Of which several thousand contain non-Latin characters
-   17 documents contain the word "search"
-   Of these, W2026888704.json has the highest score

```{data-file="tf_idf_search.csv"}
word,doc,score
…,…,…
search,W1583262424.json,0.017354843942898893
search,W1790707322.json,0.010208731731116994
search,W1978369717.json,0.022087983200053132
search,W1981216857.json,0.04189100262079043
search,W2011577929.json,0.023030124663562513
search,W2026888704.json,0.05716889769425517
search,W2032021174.json,0.022813879361557227
search,W2082863826.json,0.017734877021940473
search,W2084509015.json,0.012992931294148902
search,W2086938190.json,0.020417463462233987
search,W2101925012.json,0.02466678326909487
search,W2316979134.json,0.045842984000110276
search,W2575616999.json,0.047796947252574
search,W2892782288.json,0.020678111931964636
search,W4206540709.json,0.028252071534951684
search,W4304606284.json,0.028584448847127585
search,W4386532853.json,0.033283262356244445
…,…,…
```

-   Upon inspection, that abstract includes phrases like "Search Dropdown Menu toolbar search search input",
    which are probably a result of inaccurate web scraping
-   The good news is,
    TF-IDF is exactly the sort of thing we know how to write unit tests for

[open_alex]: https://openalex.org/
[pyalex]: https://pypi.org/project/pyalex/

# Scraping Web Data

## Documents as Data {: #scrape-dom}

-   Parse an HTML page using [Beautiful Soup][bs4]
-   Result is a tree called [DOM](g:dom) (Document Object Model)
    -   Nodes are HTML elements or text
    -   Node attributes are properties of objects
-   Read a page and visit its nodes

```{data-file="parse_page.py:main"}
def main():
    """Parse page and visit nodes."""
    options = parse_args()
    text = Path(options.filename).read_text()
    doc = BeautifulSoup(text, "html.parser")
    visit(doc, options.noblanks)
```

-   The [Visitor](g:visitor) function handles different types of nodes
    -   If the node is `NavigableString`, show the text (unless it would be blank and we've been asked not to)
    -   If it's a `Tag`, show name and attributes

```{data-file="parse_page.py:visit"}
def visit(node, noblanks, depth=0):
    """Show nodes in DOM tree."""
    prefix = "  " * depth
    if isinstance(node, NavigableString):
        if (not noblanks) or node.string.strip():
            print(f"{prefix}text: {repr(node.string)}")
    elif isinstance(node, Tag):
        print(f"{prefix}element: {node.name} with {node.attrs}")
        for child in node:
            visit(child, noblanks, depth+1)
```

-   Test on a small page

```{data-file="small.html"}
<html>
  <h1>Page Title</h1>
  <p>paragraph</p>
</html>

```
```{data-file="small.sh"}
python parse_page.py --filename small.html
```
```{data-file="small.out"}
element: [document] with {}
  element: html with {}
    text: '\n'
    element: h1 with {}
      text: 'Page Title'
    text: '\n'
    element: p with {}
      text: 'paragraph'
    text: '\n'
  text: '\n'
```

-   Try a larger page but don't show text that is just whitespace (newlines and indentation)

```{data-file="medium.html"}
<html>
  <head>
    <title>Example Page</title>
  </head>
  <body>
    <h1>Page Title</h1>
    <ul class="details">
      <li>first point</li>
      <li>second point</li>
    </ul>
  </body>
</html>
```
```{data-file="medium.sh"}
python parse_page.py --filename medium.html --noblanks
```
```{data-file="medium.out"}
element: [document] with {}
  element: html with {}
    element: head with {}
      element: title with {}
        text: 'Example Page'
    element: body with {}
      element: h1 with {}
        text: 'Page Title'
      element: ul with {'class': ['details']}
        element: li with {}
          text: 'first point'
        element: li with {}
          text: 'second point'
```

## Fetching {: #scrape-fetch}

-   Here's the part we already know

```{data-file="scrape.py:main"}
def main():
    """Main driver."""
    args = parse_args()
    homepage = get_page(args.homepage)
    result = []
    for link in homepage.find_all("a"):
        result.append(get_info(args, link["href"]))
    print(result)
```

-   Here's the part we don't

```{data-file="scrape.py:get_page"}
def get_page(url):
    """Get HTML page as soup."""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")
```

-   Use the [requests][requests] library to fetch a page at a URL
-   `response` object has many useful properties
    -   `response.text` is the result as characters
    -   `response.json()` (method call) would turn JSON-as-text into JSON-as-objects
-   And then we pull out information using Beautiful Soup

```{data-file="scrape.py:get_info"}
def get_info(args, relative):
    """Get info from staff page."""
    page = get_page(f"{args.homepage}/{relative}")
    result = {"name": page.find("h1").string}
    for row in page.find_all("tr"):
        kind = row.find("th").string.lower()
        count = int(row.find("td").string)
        result[kind] = count
    return result
```

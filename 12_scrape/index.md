# Scraping Web Data

## Documents as Data {: #scrape-dom}

-   Parse an HTML page using [Beautiful Soup][bs4]
-   Result is a tree called [%g dom "DOM" %] (Document Object Model)
    -   Nodes are HTML elements or text
    -   Node attributes are properties of objects
-   Read a page and visit its nodes

[%inc parse_page.py pattern=func:main %]

-   The [%g visitor "Visitor" %] function handles different types of nodes
    -   If the node is `NavigableString`, show the text (unless it would be blank and we've been asked not to)
    -   If it's a `Tag`, show name and attributes

[%inc parse_page.py pattern=func:visit %]

-   Test on a small page

[%inc small.html %]
[%inc small.sh %]
[%inc small.out %]

-   Try a larger page but don't show text that is just whitespace (newlines and indentation)

[%inc medium.html %]
[%inc medium.sh %]
[%inc medium.out %]

## Fetching {: #scrape-fetch}

-   Here's the part we already know

[%inc scrape.py pattern=func:main %]

-   Here's the part we don't

[%inc scrape.py pattern=func:get_page %]

-   Use the [requests][requests] library to fetch a page at a URL
-   `response` object has many useful properties
    -   `response.text` is the result as characters
    -   `response.json()` (method call) would turn JSON-as-text into JSON-as-objects
-   And then we pull out information using Beautiful Soup

[%inc scrape.py pattern=func:get_info %]

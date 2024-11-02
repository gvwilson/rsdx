# A Web Service

## Getting Data {: #serve-data}

-   Assay database from [the LIMS chapter](../10_lims/index.md)
    -   `staff`
    -   `experiment`
    -   `performed`
    -   `plate`
    -   `invalidated`
-   Use [sqlite3][sqlite3] module directly
    -   Exercise: convert to [SQLModel][sqlmodel]
-   [MVC](g:mvc) design separates [model](g:model), [controller](g:controller), and [view](g:view)
    -   Model is data storage
    -   Controller is the verbs
    -   View is the display
-   Model functions:
    -   `get_all` to get all records (but *not* 1-1 with database records)
    -   `get_count` to count records of a particular type
    -   `get_plate_filename` to turn a plate ID into an assay filename

```{data-file="model.py:get_count"}
def get_count(kind):
    """How many entries of the given kind?"""
    conn = sqlite3.connect(os.getenv("RSDX_DB_PATH"))
    if kind == "staff":
        result = conn.execute("select count(*) from staff").fetchone()
    elif kind == "experiments":
        result = conn.execute("select count(*) from experiment").fetchone()
    elif kind == "plates":
        result = conn.execute("select count(*) from plate").fetchone()
    else:
        assert False, f"Unknown kind {kind}"
    conn.close()
    return result[0]
```

## Controller {: #serve-server}

-   Use [Flask][flask]
    -   Define a function to handle a request to a particular URL
    -   Use a decorator to [route](g:route) appropriate requests to it

```{data-file="server.py:index"}
app = Flask(__name__)


@app.route("/")
def index():
    """Display data server home page."""
    page_data = {
        "site_title": SITE_TITLE,
        "num_staff": model.get_count("staff"),
        "num_experiments": model.get_count("experiments"),
        "num_plates": model.get_count("plates"),
    }
    return render_template("index.html", **page_data)
```

-   Run from the command line

```{data-file="run_server.sh"}
RSDX_DB_PATH=../../data/assays.db flask --app server run
```
```{data-file="run_server.out"}
 * Serving Flask app 'server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

-   Go to port 5000

<figure id="serve_home_page">
  <img src="serve_home_page.svg" alt="screenshot of data server home page"/>
  <figcaption>Home page of data server</figcaption>
</figure>

## Templates {: #serve-template}

-   `render_template` looks in the `templates` directory for `index.html`

```{data-file="templates/index.html"}
{% extends "base.html" %}
{% block content %}
<table>
  <thead>
    <tr><th>What</th><th>How Many</th></tr>
  </thead>
  <tbody>
    <tr><td><a href="/staff">Staff:</a></td><td>{{ num_staff }}</td></tr>
    <tr><td><a href="/experiments">Experiments:</a></td><td>{{ num_experiments }}</td></tr>
    <tr><td><a href="/plates">Plates:</a></td><td>{{ num_plates }}</td></tr>
  </tbody>
</table>
{% endblock %}
```

-   This template [extends](g:extend_template) `base.html`

```{data-file="templates/base.html"}
<!DOCTYPE html>
<html lang="en">
  <head>
    <link rel="stylesheet" href="/static/style.css">
    <title>{{ site_title }}{% if page_title %}: {{ page_title }}{% endif %}</title>
  </head>
  <body>
    <h1>{{ site_title }}{% if page_title %}: {{ page_title }}{% endif %}</h1>
    {% block content %}
    {% endblock %}
  </body>
</html>
```

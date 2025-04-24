# Research Data Viewer

A FastAPI web application for viewing tables in the research database.

## Usage

```bash
# Run with default settings (uses temp.db in current directory)
python app.py

# Run with a specific database file
python app.py --db /path/to/database.db

# Specify host and port
python app.py --host 0.0.0.0 --port 8080
```

Once running, visit http://localhost:8000 in your browser.

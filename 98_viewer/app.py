"""Snailz data viewer."""

import argparse
import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(title="Research Data Viewer")

# Set up static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Set up Jinja2 templates
templates_dir = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Database path - will be set from command line
DB_PATH = None

# Table names from the database schema
TABLES = ["assays", "machines", "persons", "specimens"]


def get_db_connection():
    """Create a connection to the SQLite database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        return conn
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with links to all tables"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "tables": TABLES}
    )


@app.get("/{table_name}", response_class=HTMLResponse)
async def show_table(request: Request, table_name: str):
    """Show the contents of the specified table"""
    if table_name not in TABLES:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]

        # Get data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Format
        return templates.TemplateResponse(
            "table.html",
            {
                "request": request,
                "table_name": table_name,
                "columns": columns,
                "rows": rows,
            },
        )
    finally:
        conn.close()


def main():
    """Run the FastAPI application."""

    parser = argparse.ArgumentParser(
        description="Run the Snailz Data Viewer web application"
    )
    parser.add_argument("--db", required=True, type=str, help="Path to SQLite database")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to bind the server to"
    )
    args = parser.parse_args()

    global DB_PATH
    DB_PATH = args.db

    print(f"Server running at http://{args.host}:{args.port} using database {DB_PATH}")

    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

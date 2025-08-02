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

# Database path - will be reset from command line
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


def get_table_data(table_name):
    """Get columns and rows from the specified table"""
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

        return columns, rows
    finally:
        conn.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with links to all tables"""
    return templates.TemplateResponse(
        "index.html", {"request": request, "tables": TABLES}
    )


@app.get("/assays", response_class=HTMLResponse)
async def show_assays(request: Request):
    """Show the assays table"""
    columns, rows = get_table_data("assays")
    return templates.TemplateResponse(
        "assays.html",
        {
            "request": request,
            "columns": columns,
            "rows": rows,
        },
    )


@app.get("/machines", response_class=HTMLResponse)
async def show_machines(request: Request):
    """Show the machines table"""
    columns, rows = get_table_data("machines")
    return templates.TemplateResponse(
        "machines.html",
        {
            "request": request,
            "columns": columns,
            "rows": rows,
        },
    )


@app.get("/persons", response_class=HTMLResponse)
async def show_persons(request: Request):
    """Show the persons table"""
    columns, rows = get_table_data("persons")
    return templates.TemplateResponse(
        "persons.html",
        {
            "request": request,
            "columns": columns,
            "rows": rows,
        },
    )


@app.get("/specimens", response_class=HTMLResponse)
async def show_specimens(request: Request):
    """Show the specimens table"""
    columns, rows = get_table_data("specimens")
    return templates.TemplateResponse(
        "specimens.html",
        {
            "request": request,
            "columns": columns,
            "rows": rows,
        },
    )


def main():
    """Run the FastAPI application."""

    parser = argparse.ArgumentParser(description="Run the Snailz Data Viewer")
    parser.add_argument("--db", required=True, type=str, help="Path to SQLite database")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    args = parser.parse_args()

    global DB_PATH
    DB_PATH = args.db
    print(f"Server running at http://{args.host}:{args.port} using database {DB_PATH}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

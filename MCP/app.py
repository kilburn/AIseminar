import os
import sqlite3
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel, Field, EmailStr
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

# Load .env (safe if missing)
load_dotenv()

DB_PATH = os.getenv("DB_PATH", "/app/db/my_database.sqlite")
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))

mcp = FastMCP(name="ContactsServer")

# ---------- Pydantic Models (with descriptions) ----------

class Contact(BaseModel):
    id: int = Field(..., description="Auto-incremented unique identifier of the contact.")
    name: str = Field(..., description="Full name of the contact.")
    email: EmailStr = Field(..., description="Unique e-mail address used as an identifier.")
    created_at: datetime = Field(..., description="Creation timestamp in UTC (YYYY-MM-DD HH:MM:SS).")


class SaveContactResult(BaseModel):
    contact: Contact = Field(..., description="The saved or updated contact record.")

class ListContactsResult(BaseModel):
    contacts: List[Contact] = Field(..., description="All contacts currently stored in the database.")


class SummarizeResult(BaseModel):
    output: str = Field(..., description="Resulting summary text produced by the prompt.")


# ---------- DB Utilities ----------

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            email      TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
        cur.execute("""
            INSERT OR IGNORE INTO contacts (name, email, created_at)
            VALUES (?, ?, ?)
        """, ("Alice Example", "alice@example.com", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    finally:
        conn.close()


# ---------- MCP: Prompts / Resources / Tools ----------

@mcp.prompt(description="Generate a prompt to summarize the provided text")
def summarize(text: str) -> SummarizeResult:
    """Generate a prompt asking to summarize the given text."""
    return SummarizeResult(output=f"Can you summarize this text: {text}")

@mcp.resource("data://contacts", description="List of all contacts in the database")
def list_contacts() -> ListContactsResult:
    """Retrieve all contacts from the database."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, created_at FROM contacts ORDER BY id ASC")
        rows = cur.fetchall()
        contacts = [
            Contact(
                id=r[0],
                name=r[1],
                email=r[2],
                created_at=datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S")
                if isinstance(r[3], str) and len(r[3]) >= 19 else datetime.fromisoformat(r[3])
            )
            for r in rows
        ]
        return ListContactsResult(contacts=contacts)
    finally:
        conn.close()

@mcp.tool(description="Save or update a contact in the database by email address")
def save_contact(name: str, email: str) -> SaveContactResult:
    """Save a new contact or update an existing one using email as unique identifier."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO contacts (name, email, created_at)
            VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                name=excluded.name
        """, (name, email, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        cur.execute("SELECT id, name, email, created_at FROM contacts WHERE email = ?", (email,))
        row = cur.fetchone()
        contact = Contact(
            id=row[0],
            name=row[1],
            email=row[2],
            created_at=datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
            if isinstance(row[3], str) and len(row[3]) >= 19 else datetime.fromisoformat(row[3])
        )
        return SaveContactResult(contact=contact)
    finally:
        conn.close()


# ---------- Healthcheck via FastMCP custom route ----------

@mcp.custom_route("/health", methods=["GET"])
async def health_check(_: Request):
    """
    Liveness/Readiness probe: just verify we can open the DB and execute a trivial query.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        _ = cur.fetchone()
        conn.close()
        return JSONResponse({"status": "ok"})
    except Exception as e:
        return JSONResponse({"status": "error", "error": str(e)}, status_code=503)


# ---------- Start ----------

if __name__ == "__main__":
    init_db()
    mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT)

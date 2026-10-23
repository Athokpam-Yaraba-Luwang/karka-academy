# Karka AI & Tech Academy website · SiteSprint, Karka Infini AI 2026
# Built by Athokpam Yaraba Luwang · https://www.linkedin.com/in/yaraba-athokpam-856538343/
"""Tiny SQLite lead store. One connection per call keeps it thread-safe."""

from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(os.getenv("DATA_DIR", Path(__file__).resolve().parent.parent / "data")) / "leads.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT    NOT NULL,
    name       TEXT    NOT NULL,
    phone      TEXT    NOT NULL,
    email      TEXT,
    program    TEXT    NOT NULL,
    audience   TEXT,
    message    TEXT,
    source     TEXT
)
"""

FIELDS = ("id", "created_at", "name", "phone", "email", "program", "audience", "message", "source")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(SCHEMA)
    return conn


def save_lead(lead: dict) -> int:
    with closing(_connect()) as conn, conn:
        cur = conn.execute(
            "INSERT INTO leads (created_at, name, phone, email, program, audience, message, source)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                lead["name"],
                lead["phone"],
                lead.get("email") or None,
                lead["program"],
                lead.get("audience") or None,
                lead.get("message") or None,
                lead.get("source") or None,
            ),
        )
        return int(cur.lastrowid)


def list_leads(limit: int = 500) -> list[dict]:
    with closing(_connect()) as conn:
        rows = conn.execute(
            f"SELECT {', '.join(FIELDS)} FROM leads ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(zip(FIELDS, r)) for r in rows]

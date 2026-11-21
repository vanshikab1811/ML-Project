"""Opt-in history storage in SQLite.

Stores only the job title, date, scores and skill lists of an analysis.
Resume text and contact details are never written here.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "resumeiq.db"

_SCORE_KEYS = (
    "required_skill_coverage",
    "preferred_skill_coverage",
    "text_similarity",
    "keyword_coverage",
    "experience_relevance",
)
_SKILL_KEYS = ("matched", "missing_required", "missing_preferred", "extra")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            overall REAL NOT NULL,
            scores TEXT NOT NULL,
            skills TEXT NOT NULL
        )"""
    )
    return conn


def save_analysis(job_title: str, match_result: dict) -> int:
    """Save one analysis. Returns the new record id."""
    scores = {k: match_result["components"][k] for k in _SCORE_KEYS}
    skills = {k: list(match_result[k]) for k in _SKILL_KEYS}
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO analyses (job_title, created_at, overall, scores, skills) VALUES (?, ?, ?, ?, ?)",
            (
                job_title,
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                float(match_result["overall"]),
                json.dumps(scores),
                json.dumps(skills),
            ),
        )
        return cur.lastrowid


def list_analyses(job_title: str | None = None, limit: int | None = None) -> list:
    """Saved analyses, newest first. Each item has id, job_title, created_at, overall, scores, skills."""
    query = "SELECT * FROM analyses"
    params: list = []
    if job_title is not None:
        query += " WHERE job_title = ?"
        params.append(job_title)
    query += " ORDER BY created_at DESC, id DESC"
    if limit is not None:
        query += " LIMIT ?"
        params.append(limit)
    conn = _connect()
    try:
        rows = conn.execute(query, params).fetchall()
    finally:
        conn.close()
    return [
        {
            "id": r["id"],
            "job_title": r["job_title"],
            "created_at": r["created_at"],
            "overall": r["overall"],
            "scores": json.loads(r["scores"]),
            "skills": json.loads(r["skills"]),
        }
        for r in rows
    ]


def delete_analysis(analysis_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))


def delete_all() -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM analyses")


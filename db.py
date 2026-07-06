import os
import sqlite3
from datetime import datetime

DB_PATH = os.environ.get("DATABASE_PATH", "storage/app.db")


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id TEXT UNIQUE NOT NULL,
                original_files TEXT NOT NULL,
                output_file TEXT NOT NULL,
                pdf_count INTEGER DEFAULT 0,
                row_count INTEGER DEFAULT 0,
                duplicate_count INTEGER DEFAULT 0,
                total_credit REAL DEFAULT 0,
                status TEXT DEFAULT 'OK',
                error TEXT DEFAULT '',
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def add_job(job):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO jobs (job_id, original_files, output_file, pdf_count, row_count,
                              duplicate_count, total_credit, status, error, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job["job_id"], job["original_files"], job["output_file"], job["pdf_count"],
                job["row_count"], job["duplicate_count"], job["total_credit"], job["status"],
                job.get("error", ""), datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )
        conn.commit()


def recent_jobs(limit=20):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM jobs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()


def find_job(job_id):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,)).fetchone()


def dashboard_stats():
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) jobs, COALESCE(SUM(pdf_count),0) pdfs, COALESCE(SUM(row_count),0) rows, COALESCE(SUM(total_credit),0) credit FROM jobs"
        ).fetchone()
        return dict(row)

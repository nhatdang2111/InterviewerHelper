"""SQLite database operations"""
import sqlite3
import json
from pathlib import Path
from typing import List, Optional
from .models import CVRecord, Settings
from core.encryption import encrypt, decrypt, is_encrypted


class Database:
    """SQLite database wrapper"""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "history.db"
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize database tables"""
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cv_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidate_name TEXT,
                    position TEXT,
                    cv_text TEXT,
                    cv_summary TEXT,
                    jd_text TEXT,
                    questions TEXT,
                    score INTEGER DEFAULT 0,
                    score_breakdown TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
            """)
            conn.commit()

    # CV Records
    def save_cv_record(self, record: CVRecord) -> int:
        """Save CV record and return ID"""
        with self._get_conn() as conn:
            cursor = conn.execute("""
                INSERT INTO cv_records
                (candidate_name, position, cv_text, cv_summary, jd_text, questions, score, score_breakdown)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.candidate_name,
                record.position,
                record.cv_text,
                record.cv_summary,
                record.jd_text,
                record.questions,
                record.score,
                record.score_breakdown
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_records(self) -> List[CVRecord]:
        """Get all CV records"""
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT * FROM cv_records ORDER BY created_at DESC"
            ).fetchall()

            return [CVRecord(
                id=row["id"],
                candidate_name=row["candidate_name"],
                position=row["position"],
                cv_text=row["cv_text"],
                cv_summary=row["cv_summary"],
                jd_text=row["jd_text"],
                questions=row["questions"],
                score=row["score"],
                score_breakdown=row["score_breakdown"],
                created_at=row["created_at"]
            ) for row in rows]

    def get_record(self, record_id: int) -> Optional[CVRecord]:
        """Get single CV record by ID"""
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM cv_records WHERE id = ?", (record_id,)
            ).fetchone()

            if row:
                return CVRecord(
                    id=row["id"],
                    candidate_name=row["candidate_name"],
                    position=row["position"],
                    cv_text=row["cv_text"],
                    cv_summary=row["cv_summary"],
                    jd_text=row["jd_text"],
                    questions=row["questions"],
                    score=row["score"],
                    score_breakdown=row["score_breakdown"],
                    created_at=row["created_at"]
                )
            return None

    def delete_record(self, record_id: int):
        """Delete CV record"""
        with self._get_conn() as conn:
            conn.execute("DELETE FROM cv_records WHERE id = ?", (record_id,))
            conn.commit()

    # Settings
    # Keys that contain sensitive data requiring encryption
    _SENSITIVE_KEYS = {"claude_api_key", "gemini_api_key"}

    def save_settings(self, settings: Settings):
        """Save app settings with encryption for sensitive values"""
        with self._get_conn() as conn:
            for key, value in settings.__dict__.items():
                # Encrypt sensitive keys before storage
                if key in self._SENSITIVE_KEYS and value:
                    value = encrypt(value)
                conn.execute(
                    "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                    (key, value)
                )
            conn.commit()

    def load_settings(self) -> Settings:
        """Load app settings with decryption for sensitive values"""
        settings = Settings()
        with self._get_conn() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
            for key, value in rows:
                if hasattr(settings, key):
                    # Decrypt sensitive keys after loading
                    if key in self._SENSITIVE_KEYS and value:
                        value = decrypt(value)
                    setattr(settings, key, value)
        return settings

    def migrate_plaintext_keys(self):
        """Migrate existing plaintext API keys to encrypted format.

        Safe to call multiple times - skips already encrypted values.
        """
        with self._get_conn() as conn:
            for key in self._SENSITIVE_KEYS:
                row = conn.execute(
                    "SELECT value FROM settings WHERE key = ?", (key,)
                ).fetchone()
                if row and row[0] and not is_encrypted(row[0]):
                    encrypted_value = encrypt(row[0])
                    conn.execute(
                        "UPDATE settings SET value = ? WHERE key = ?",
                        (encrypted_value, key)
                    )
            conn.commit()

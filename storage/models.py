"""Data models for storage"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CVRecord:
    """Record of analyzed CV"""
    id: Optional[int] = None
    candidate_name: str = ""
    position: str = ""
    cv_text: str = ""
    cv_summary: str = ""
    jd_text: str = ""
    questions: str = ""
    score: int = 0
    score_breakdown: str = ""  # JSON string
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Settings:
    """App settings"""
    claude_api_key: str = ""
    gemini_api_key: str = ""
    default_model: str = "gemini"
    language: str = "en"

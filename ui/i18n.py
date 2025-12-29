"""Internationalization support for Vietnamese and English"""

LANGUAGES = {
    "en": "English",
    "vi": "Tiếng Việt"
}

_current_language = "en"

TRANSLATIONS = {
    "app_title": {
        "en": "Interviewer Helper",
        "vi": "Trợ Lý Phỏng Vấn"
    },
    "tab_generate": {
        "en": "Generate Questions",
        "vi": "Tạo Câu Hỏi"
    },
    "tab_history": {
        "en": "History",
        "vi": "Lịch Sử"
    },
    "tab_compare": {
        "en": "Compare CVs",
        "vi": "So Sánh CV"
    },
    "tab_settings": {
        "en": "Settings",
        "vi": "Cài Đặt"
    },
    "upload_cv": {
        "en": "Upload CV (PDF)",
        "vi": "Tải CV (PDF)"
    },
    "job_description": {
        "en": "Job Description",
        "vi": "Mô Tả Công Việc"
    },
    "jd_freetext": {
        "en": "Free Text",
        "vi": "Văn Bản Tự Do"
    },
    "jd_structured": {
        "en": "Structured",
        "vi": "Có Cấu Trúc"
    },
    "required_skills": {
        "en": "Required Skills",
        "vi": "Kỹ Năng Bắt Buộc"
    },
    "nice_to_have": {
        "en": "Nice to Have",
        "vi": "Kỹ Năng Ưu Tiên"
    },
    "experience_years": {
        "en": "Years of Experience",
        "vi": "Số Năm Kinh Nghiệm"
    },
    "select_model": {
        "en": "Select AI Model",
        "vi": "Chọn AI Model"
    },
    "generate": {
        "en": "Generate Questions",
        "vi": "Tạo Câu Hỏi"
    },
    "download": {
        "en": "Download .md",
        "vi": "Tải File .md"
    },
    "api_keys": {
        "en": "API Keys",
        "vi": "API Keys"
    },
    "save_settings": {
        "en": "Save Settings",
        "vi": "Lưu Cài Đặt"
    },
    "language": {
        "en": "Language",
        "vi": "Ngôn Ngữ"
    },
    "candidate_name": {
        "en": "Candidate Name",
        "vi": "Tên Ứng Viên"
    },
    "position": {
        "en": "Position",
        "vi": "Vị Trí"
    },
    "score": {
        "en": "Score",
        "vi": "Điểm"
    },
    "date": {
        "en": "Date",
        "vi": "Ngày"
    },
    "actions": {
        "en": "Actions",
        "vi": "Thao Tác"
    },
    "view": {
        "en": "View",
        "vi": "Xem"
    },
    "delete": {
        "en": "Delete",
        "vi": "Xóa"
    },
    "select_cvs": {
        "en": "Select CVs to Compare",
        "vi": "Chọn CV Để So Sánh"
    },
    "compare": {
        "en": "Compare",
        "vi": "So Sánh"
    },
    "processing": {
        "en": "Processing...",
        "vi": "Đang xử lý..."
    },
    "success": {
        "en": "Success!",
        "vi": "Thành công!"
    },
    "error": {
        "en": "Error",
        "vi": "Lỗi"
    }
}


def set_language(lang: str):
    """Set current language"""
    global _current_language
    if lang in LANGUAGES:
        _current_language = lang


def get_text(key: str) -> str:
    """Get translated text for key"""
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(_current_language, TRANSLATIONS[key]["en"])
    return key

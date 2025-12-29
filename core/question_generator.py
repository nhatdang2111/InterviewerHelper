"""Generate interview questions from CV and JD"""
from .ai_client import AIClient
from .prompt_templates import CV_ANALYSIS_PROMPT, QUESTION_GENERATION_PROMPT


def analyze_cv(ai_client: AIClient, cv_text: str, model: str = "gemini") -> str:
    """Analyze CV and extract structured information (text-based).

    Args:
        ai_client: Configured AI client
        cv_text: Raw text from CV PDF
        model: "claude" or "gemini"

    Returns:
        Structured CV summary in markdown
    """
    prompt = CV_ANALYSIS_PROMPT.format(cv_text=cv_text)
    return ai_client.chat(prompt, model_provider=model)


def analyze_cv_from_pdf(
    ai_client: AIClient,
    pdf_bytes: bytes,
    model: str = "gemini"
) -> str:
    """Analyze CV directly from PDF using AI vision.

    Use this for image-based/scanned PDFs where text extraction fails.

    Args:
        ai_client: Configured AI client
        pdf_bytes: PDF file as bytes
        model: "claude" or "gemini"

    Returns:
        Structured CV summary in markdown
    """
    prompt = """Analyze this resume/CV document and extract structured information.

Extract and return:
1. **Full Name** and contact info (location, email if visible)
2. **Professional Summary** (2-3 sentences)
3. **Work Experience** (company, role, dates, key achievements for each)
4. **Technical Skills** (categorized: backend, frontend, database, cloud, tools)
5. **Education** (degree, school, year)
6. **Certifications** (if any)

Format as structured markdown."""

    return ai_client.chat_with_pdf(prompt, pdf_bytes, model_provider=model)


def generate_interview_questions(
    ai_client: AIClient,
    cv_summary: str,
    jd_text: str,
    model: str = "gemini"
) -> str:
    """Generate interview questions based on CV and JD.

    Args:
        ai_client: Configured AI client
        cv_summary: Analyzed CV summary
        jd_text: Job description text
        model: "claude" or "gemini"

    Returns:
        Interview questions in markdown format
    """
    prompt = QUESTION_GENERATION_PROMPT.format(
        cv_summary=cv_summary,
        jd_text=jd_text
    )
    return ai_client.chat(prompt, model_provider=model)

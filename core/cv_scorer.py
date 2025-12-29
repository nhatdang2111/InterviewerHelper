"""CV scoring logic"""
import json
from .ai_client import AIClient
from .prompt_templates import SCORING_PROMPT


def score_cv(
    ai_client: AIClient,
    cv_summary: str,
    jd_text: str,
    model: str = "gemini"
) -> dict:
    """Score CV against job description.

    Args:
        ai_client: Configured AI client
        cv_summary: Analyzed CV summary
        jd_text: Job description
        model: "claude" or "gemini"

    Returns:
        Score breakdown dict
    """
    prompt = SCORING_PROMPT.format(
        cv_summary=cv_summary,
        jd_text=jd_text
    )

    response = ai_client.chat(prompt, model_provider=model)

    # Extract JSON from response
    try:
        # Find JSON block in response
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        if json_start != -1 and json_end > json_start:
            json_str = response[json_start:json_end]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # Fallback if parsing fails
    return {
        "overall_score": 0,
        "error": "Failed to parse score",
        "raw_response": response
    }

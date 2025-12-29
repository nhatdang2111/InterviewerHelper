"""AI prompt templates for CV analysis and question generation"""

CV_ANALYSIS_PROMPT = """Analyze this resume and extract structured information.

Resume content:
{cv_text}

Extract and return:
1. **Full Name** and contact info (location, email if visible)
2. **Professional Summary** (2-3 sentences)
3. **Work Experience** (company, role, dates, key achievements for each)
4. **Technical Skills** (categorized: backend, frontend, database, cloud, tools)
5. **Education** (degree, school, year)
6. **Certifications** (if any)

Format as structured markdown."""


QUESTION_GENERATION_PROMPT = """You are an expert technical interviewer. Based on the CV analysis and Job Description, generate comprehensive interview questions.

## CV Summary:
{cv_summary}

## Job Description:
{jd_text}

## Generate questions in these categories:

### 1. Technical Deep-Dive (6-8 questions)
Verify claimed technical skills. Ask about specific technologies mentioned in CV.

### 2. Experience Validation (4-6 questions)
Verify work experience claims. Ask about specific projects, achievements, numbers.

### 3. Scenario-Based (4-6 questions)
Problem-solving scenarios relevant to the job requirements.

### 4. Independent Work & AI Usage (3-4 questions)
Assess ability to work independently and use AI tools productively.

### 5. Growth Mindset (3-4 questions)
Evaluate learning ability, adaptability, career goals.

### 6. Red Flags to Probe (2-4 questions)
Address any gaps, inconsistencies, or concerns from CV.

## Output Format:
For each category, create a markdown table:
| # | Question | Purpose |
|---|----------|---------|

Also include a brief "Assessment Notes" section highlighting:
- Key strengths to validate
- Potential concerns to explore
- Recommended focus areas"""


SCORING_PROMPT = """Score this candidate's fit for the position (0-100).

## CV Summary:
{cv_summary}

## Job Description Requirements:
{jd_text}

## Scoring Criteria:
1. **Required Skills Match** (40 points max)
   - Each must-have skill from JD found in CV

2. **Experience Level** (25 points max)
   - Years of experience vs JD requirement
   - Relevance of past roles

3. **Nice-to-Have Skills** (20 points max)
   - Bonus skills that add value

4. **Education Relevance** (10 points max)
   - Degree match, certifications

5. **Tech Stack Modernity** (5 points max)
   - Using current/modern technologies

## Output as JSON:
```json
{{
  "overall_score": <0-100>,
  "breakdown": {{
    "required_skills": {{ "score": <0-40>, "matched": [...], "missing": [...] }},
    "experience_level": {{ "score": <0-25>, "notes": "..." }},
    "nice_to_have": {{ "score": <0-20>, "matched": [...] }},
    "education": {{ "score": <0-10>, "notes": "..." }},
    "tech_modernity": {{ "score": <0-5>, "notes": "..." }}
  }},
  "summary": "2-3 sentence assessment",
  "recommendation": "Strong Hire | Hire | Maybe | No Hire"
}}
```"""


COMPARE_CVS_PROMPT = """Compare these candidates for the same position.

## Job Description:
{jd_text}

## Candidates:
{candidates_summaries}

## For each candidate provide:
1. Overall match score (0-100)
2. Top 3 strengths for this role
3. Top 3 concerns/gaps
4. Unique differentiator

## Output as comparison table:
| Aspect | {candidate_names} |
|--------|-------------------|

End with a ranking recommendation and rationale."""

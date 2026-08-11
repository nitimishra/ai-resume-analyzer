import json
from resume_analyzer import client


def analyze_job(job_description: str) -> dict:
    """
    Analyzes a job description and extracts required skills.
    """

    prompt = f"""
You are an expert job description parser. Analyze the following job description and extract structured requirements.

Return ONLY a valid JSON object (no markdown, no explanation, no code fences) with exactly this structure:

{{
  "required_skills": ["list of must-have skills/technologies"],
  "preferred_skills": ["list of nice-to-have skills"],
  "experience_required": "short string, e.g. '2+ years' or 'Not specified'",
  "education_required": "short string, e.g. 'Bachelor's degree' or 'Not specified'",
  "tools": ["list of tools/software mentioned"],
  "responsibilities": ["list of 2-4 key responsibilities"],
  "keywords": ["list of important keywords from the posting"]
}}

If a category has no information, return an empty list or "Not specified" as appropriate.

Job description:
\"\"\"
{job_description}
\"\"\"
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:].strip()

        parsed = json.loads(raw_text)
        return parsed

    except Exception as e:
        print(f"Job analysis failed: {e}")
        return {}
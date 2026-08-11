import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_resume(resume_text: str) -> dict:
    prompt = f"""
You are an expert resume parser. Analyze the following resume text and extract structured information.

Return ONLY a valid JSON object (no markdown, no explanation, no code fences) with exactly this structure:

{{
  "skills": ["list of general skills"],
  "programming_languages": ["list of languages"],
  "frameworks": ["list of frameworks/libraries"],
  "tools": ["list of tools/software"],
  "education": ["list of degrees/institutions"],
  "experience": ["list of past roles/internships with brief context"],
  "projects": ["list of project names with 1-line description each"],
  "certifications": ["list of certifications"],
  "domains": ["list of relevant domains, e.g. Machine Learning, Web Development"],
  "possible_roles": ["list of 3-5 job titles this person is suited for"]
}}

If a category has no information, return an empty list for it.

Resume text:
\"\"\"
{resume_text}
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
        print(f"Resume analysis failed: {e}")
        return {}
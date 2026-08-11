def normalize_skill(skill: str) -> str:
    return skill.strip().lower()


def calculate_match(resume_analysis: dict, job_analysis: dict) -> dict:
    """
    Compares resume skills with job requirements.
    Returns match_percentage, matched_skills, missing_skills
    """

    resume_skills = set()
    for key in ["skills", "programming_languages", "frameworks", "tools"]:
        for s in resume_analysis.get(key, []):
            resume_skills.add(normalize_skill(s))

    job_required = job_analysis.get("required_skills", []) + job_analysis.get("tools", [])
    job_required_normalized = list(set(normalize_skill(s) for s in job_required if s.strip()))

    if not job_required_normalized:
        return {
            "match_percentage": None,
            "matched_skills": [],
            "missing_skills": [],
            "insufficient_data": True
        }

    matched = []
    missing = []

    for req_skill in job_required_normalized:
        found = False
        for res_skill in resume_skills:
            if req_skill == res_skill or req_skill in res_skill or res_skill in req_skill:
                found = True
                break
        if found:
            matched.append(req_skill)
        else:
            missing.append(req_skill)

    match_percentage = round((len(matched) / len(job_required_normalized)) * 100)

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched,
        "missing_skills": missing
    }
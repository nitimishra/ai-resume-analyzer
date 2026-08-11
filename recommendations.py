def generate_recommendations(missing_skills: list) -> list:
    """
    Generates simple, actionable recommendations for missing skills.
    """

    recommendations = []

    for skill in missing_skills:
        recommendations.append({
            "skill": skill.title(),
            "suggestion": f"Learn {skill.title()} fundamentals and build one small project using it to strengthen your profile for this role."
        })

    return recommendations
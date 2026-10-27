def generate_roadmap(missing_skills):
    if not missing_skills:
        return "Great! No major skill gaps were found for this role."

    roadmap = "### Suggested Learning Roadmap\n"

    week = 1

    for skill in missing_skills[:4]:
        roadmap += f"- **Week {week}:** Learn the basics of **{skill}** and build one small practice project.\n"
        week += 1

    roadmap += "\n**Tip:** Add these skills to your resume only after completing practical projects."

    return roadmap
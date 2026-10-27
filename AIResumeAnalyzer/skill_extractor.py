import pandas as pd

def load_skill_dictionary(path="data/skill_dictionary.csv"):
    skill_df = pd.read_csv(path, encoding="utf-8-sig")

    skill_df.columns = (
        skill_df.columns
        .str.strip()
        .str.lower()
    )

    required_columns = {"skill", "category"}

    if not required_columns.issubset(skill_df.columns):
        raise ValueError(
            "skill_dictionary.csv must have the headings: skill,category. "
            f"Headings currently found: {skill_df.columns.tolist()}"
        )

    skill_df = skill_df.dropna(subset=["skill", "category"])

    return skill_df

def extract_skills(resume_text, skill_df):
    resume_text = resume_text.lower()
    found_skills = []

    for skill in skill_df["skill"]:
        if skill.lower() in resume_text:
            found_skills.append(skill)

    return sorted(set(found_skills))

def group_skills(found_skills, skill_df):
    groups = {}

    for skill in found_skills:
        category = skill_df.loc[
            skill_df["skill"] == skill, "category"
        ].values[0]

        if category not in groups:
            groups[category] = []

        groups[category].append(skill)

    return groups
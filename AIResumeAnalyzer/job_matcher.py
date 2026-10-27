import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_job_roles(path="data/job_roles.csv"):
    job_roles_df = pd.read_csv(path, encoding="utf-8-sig")

    job_roles_df.columns = (
        job_roles_df.columns
        .str.strip()
        .str.lower()
    )

    required_columns = {"job_role", "required_skills"}

    if not required_columns.issubset(job_roles_df.columns):
        raise ValueError(
            "job_roles.csv must have the headings: "
            "job_role,required_skills. "
            f"Headings currently found: {job_roles_df.columns.tolist()}"
        )

    job_roles_df = job_roles_df.dropna(
        subset=["job_role", "required_skills"]
    )

    return job_roles_df

def calculate_match_scores(resume_text, job_roles_df):
    resume_text = resume_text.lower()

    job_texts = job_roles_df["required_skills"].str.lower().tolist()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text] + job_texts)

    resume_vector = vectors[0]
    job_vectors = vectors[1:]

    similarity_scores = cosine_similarity(resume_vector, job_vectors)[0]

    job_roles_df["match_score"] = (similarity_scores * 100).round(2)

    return job_roles_df.sort_values(
        by="match_score", ascending=False
    ).reset_index(drop=True)

def get_skill_gap(resume_skills, required_skills):
    resume_skills = [skill.lower() for skill in resume_skills]
    required_skills = [skill.strip() for skill in required_skills.split(",")]

    found = []
    missing = []

    for skill in required_skills:
        if skill.lower() in resume_skills:
            found.append(skill)
        else:
            missing.append(skill)

    return found, missing
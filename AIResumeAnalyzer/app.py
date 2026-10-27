import streamlit as st
import pandas as pd
import plotly.express as px

from resume_parser import extract_resume_text
from text_cleaner import clean_text
from skill_extractor import load_skill_dictionary, extract_skills, group_skills
from job_matcher import load_job_roles, calculate_match_scores, get_skill_gap
from roadmap_generator import generate_roadmap

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer and Job Recommendation System")
st.caption("Upload your resume to find suitable job roles, skill gaps, and a learning roadmap.")

skill_df = load_skill_dictionary()
job_roles_df = load_job_roles()

uploaded_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file is not None:
    st.success(f"Uploaded file: **{uploaded_file.name}**")

    try:
        raw_text = extract_resume_text(uploaded_file)
        cleaned_text = clean_text(raw_text)

        if len(cleaned_text) < 50:
            st.error("Could not extract enough text. Please upload a text-based PDF or DOCX resume.")
            st.stop()

        found_skills = extract_skills(cleaned_text, skill_df)
        skill_groups = group_skills(found_skills, skill_df)

        st.subheader("✅ Skills Found in Your Resume")

        if found_skills:
            for category, skills in skill_groups.items():
                st.markdown(f"**{category}:** {', '.join(skills)}")
        else:
            st.warning("No known skills were detected. Try adding a Skills section to your resume.")

        st.subheader("🎯 Job Role Match Scores")

        ranked_roles = calculate_match_scores(cleaned_text, job_roles_df)

        top_roles = ranked_roles.head(3)

        for index, row in top_roles.iterrows():
            st.markdown(
                f"### {index + 1}. {row['job_role']} — {row['match_score']:.2f}%"
            )

        fig = px.bar(
            ranked_roles.head(5),
            x="match_score",
            y="job_role",
            orientation="h",
            text="match_score",
            title="Top 5 Job Role Matches",
            labels={
                "match_score": "Match Score (%)",
                "job_role": "Job Role"
            }
        )

        fig.update_layout(yaxis={"categoryorder": "total ascending"})

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("🔍 Skill Gap Analysis")

        selected_role = st.selectbox(
            "Select a target job role",
            job_roles_df["job_role"].tolist()
        )

        selected_role_data = job_roles_df[
            job_roles_df["job_role"] == selected_role
        ].iloc[0]

        required_skills = selected_role_data["required_skills"]

        matched_skills, missing_skills = get_skill_gap(
            found_skills,
            required_skills
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### ✅ Skills You Have")
            st.write(", ".join(matched_skills) if matched_skills else "None found")

        with col2:
            st.markdown("#### ❌ Missing Skills")
            st.write(", ".join(missing_skills) if missing_skills else "None")

        st.markdown(generate_roadmap(missing_skills))

        report_data = {
            "Uploaded Resume": [uploaded_file.name],
            "Selected Role": [selected_role],
            "Match Score": [f"{ranked_roles.loc[ranked_roles['job_role'] == selected_role, 'match_score'].values[0]:.2f}%"],
            "Skills Found": [", ".join(found_skills)],
            "Missing Skills": [", ".join(missing_skills)]
        }

        report_df = pd.DataFrame(report_data)

        csv_report = report_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Analysis Report",
            data=csv_report,
            file_name="resume_analysis_report.csv",
            mime="text/csv"
        )

    except Exception as error:
        st.error(f"Something went wrong while processing the resume: {error}")

else:
    st.info("Please upload a PDF or DOCX resume to begin.")
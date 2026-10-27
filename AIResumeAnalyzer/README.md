# AI Resume Analyzer and Job Recommendation System

This is a Streamlit-based application that analyzes a student's resume and recommends suitable job roles.

## Features

- Upload PDF or DOCX resumes
- Extract and clean resume text
- Detect technical skills
- Compare resume with multiple job roles
- Calculate match scores using TF-IDF and cosine similarity
- Recommend the top three job roles
- Identify missing skills
- Generate a learning roadmap
- Download an analysis report

## Technologies Used

- Python
- Streamlit
- pandas
- NumPy
- scikit-learn
- pypdf
- python-docx
- Plotly

## How to Run

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Important Note

This tool provides educational guidance only. It does not make hiring decisions and should not be used to reject candidates automatically.
Upload PDF / DOCX Resume
            ↓
Extract Resume Text
            ↓
Clean and Normalize Text
            ↓
      ┌─────┴──────────────────────┐
      ↓                            ↓
Detect Skills                 Load Job Roles
Using Skill Dictionary             ↓
      ↓                    TF-IDF Vectorization
      │                            ↓
      │                    Cosine Similarity
      │                            ↓
      │                    Rank Roles + Top 3
      │
      └────────────┬────────────────┘
                   ↓
          Select Target Role
                   ↓
      Compare Detected / Required Skills
                   ↓
       Missing Skills + Learning Roadmap
                   ↓
       Dashboard + Downloadable CSV
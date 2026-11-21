"""Sample data matching docs/ui_contracts.md. Replace with src/ output later."""
from copy import deepcopy

_RESUME = {
    "text": (
        "Aarav Mehta\n\nSUMMARY\nThird-year computer science student focused on data analysis and "
        "machine learning.\n\nEDUCATION\nB.Tech Computer Science, 2023-2027. CGPA 8.4.\n\n"
        "EXPERIENCE\nData analyst intern, Northwind Analytics (Jun-Aug 2025). Built SQL reports and a "
        "Pandas pipeline that cut weekly reporting time by 40%.\n\n"
        "PROJECTS\nChurn prediction: Scikit-learn logistic regression on telecom data.\n"
        "Resume keyword extractor: Python and regular expressions.\n\n"
        "SKILLS\nPython, SQL, Pandas, NumPy, Scikit-learn, Git, Flask, Matplotlib"
    ),
    "sections": {
        "summary": True,
        "education": True,
        "experience": True,
        "projects": True,
        "skills": True,
        "certifications": False,
    },
    "skills_by_category": {
        "Programming": ["Python", "SQL"],
        "Machine Learning": ["Scikit-learn", "Regression", "Classification"],
        "Data": ["Pandas", "NumPy", "Matplotlib"],
        "Web/Backend": ["Flask"],
        "Tools": ["Git"],
    },
    "keywords": [
        {"term": "data pipeline", "section": "experience", "snippet": "Built SQL reports and a Pandas pipeline"},
        {"term": "logistic regression", "section": "projects", "snippet": "Scikit-learn logistic regression on telecom data"},
        {"term": "reporting", "section": "experience", "snippet": "cut weekly reporting time by 40%"},
        {"term": "classification", "section": "projects", "snippet": "Churn prediction: classification on telecom data"},
        {"term": "regular expressions", "section": "projects", "snippet": "Python and regular expressions"},
    ],
}

_JOBS = [
    {
        "title": "Data Analyst",
        "required_skills": ["SQL", "Python", "Pandas", "Data Visualization", "Excel"],
        "preferred_skills": ["Power BI", "Statistics", "Tableau"],
        "responsibilities": [
            "Build and maintain weekly reporting dashboards",
            "Query production databases to answer business questions",
            "Present findings to non-technical stakeholders",
        ],
        "keywords": ["reporting", "dashboard", "stakeholders", "data pipeline"],
        "experience_terms": ["1+ years", "bachelor's degree"],
    },
    {
        "title": "Machine Learning Engineer",
        "required_skills": ["Python", "Scikit-learn", "TensorFlow", "SQL", "Docker"],
        "preferred_skills": ["PyTorch", "AWS", "MLOps"],
        "responsibilities": [
            "Train and evaluate classification and regression models",
            "Package models for deployment as services",
            "Monitor model performance after release",
        ],
        "keywords": ["classification", "regression", "deployment", "model evaluation"],
        "experience_terms": ["2+ years", "bachelor's or master's degree"],
    },
    {
        "title": "Backend Developer",
        "required_skills": ["Python", "Flask", "REST API", "PostgreSQL", "Git"],
        "preferred_skills": ["Docker", "AWS", "Redis"],
        "responsibilities": [
            "Design and implement REST endpoints",
            "Write tests and review code",
            "Maintain database schemas",
        ],
        "keywords": ["api", "endpoints", "testing", "schema"],
        "experience_terms": ["1+ years", "computer science degree"],
    },
]

_MATCHES = {
    "Data Analyst": {
        "overall": 72.0,
        "components": {
            "required_skill_coverage": 80.0,
            "preferred_skill_coverage": 0.0,
            "text_similarity": 64.0,
            "keyword_coverage": 75.0,
            "experience_relevance": 70.0,
        },
        "weights": {"skill": 0.5, "text": 0.3, "experience": 0.2},
        "matched": ["SQL", "Python", "Pandas", "Data Visualization"],
        "missing_required": ["Excel"],
        "missing_preferred": ["Power BI", "Statistics", "Tableau"],
        "extra": ["Scikit-learn", "NumPy", "Flask", "Git"],
        "explanation": (
            "Four of five required skills appear in the resume. Text similarity is moderate because the "
            "resume leans toward modelling while the job emphasises reporting. None of the preferred "
            "skills were found."
        ),
    },
    "Machine Learning Engineer": {
        "overall": 51.0,
        "components": {
            "required_skill_coverage": 60.0,
            "preferred_skill_coverage": 0.0,
            "text_similarity": 48.0,
            "keyword_coverage": 50.0,
            "experience_relevance": 45.0,
        },
        "weights": {"skill": 0.5, "text": 0.3, "experience": 0.2},
        "matched": ["Python", "Scikit-learn", "SQL"],
        "missing_required": ["TensorFlow", "Docker"],
        "missing_preferred": ["PyTorch", "AWS", "MLOps"],
        "extra": ["Pandas", "NumPy", "Flask", "Git", "Matplotlib"],
        "explanation": (
            "Three of five required skills were found. Deployment tooling is absent from the resume, "
            "and the experience listed is closer to analysis than to model serving."
        ),
    },
    "Backend Developer": {
        "overall": 44.0,
        "components": {
            "required_skill_coverage": 60.0,
            "preferred_skill_coverage": 0.0,
            "text_similarity": 30.0,
            "keyword_coverage": 25.0,
            "experience_relevance": 35.0,
        },
        "weights": {"skill": 0.5, "text": 0.3, "experience": 0.2},
        "matched": ["Python", "Flask", "Git"],
        "missing_required": ["REST API", "PostgreSQL"],
        "missing_preferred": ["Docker", "AWS", "Redis"],
        "extra": ["SQL", "Pandas", "Scikit-learn", "NumPy"],
        "explanation": (
            "Flask and Git are present, but no API or database-administration work is described. "
            "Text overlap with the job is low."
        ),
    },
}

_RECOMMENDATIONS = [
    {
        "skill": "Excel",
        "priority": "high",
        "reason": "Required by the Data Analyst role and not found in the resume.",
        "project_name": "Monthly sales workbook",
        "learning_action": "Practise pivot tables, lookup functions and charts on a public sales dataset.",
        "resource_url": "https://support.microsoft.com/excel",
    },
    {
        "skill": "Docker",
        "priority": "high",
        "reason": "Required by Machine Learning Engineer and preferred by Backend Developer.",
        "project_name": "Containerised churn model API",
        "learning_action": "Wrap the existing churn model in a Flask service and run it in a container.",
        "resource_url": "https://docs.docker.com/get-started/",
    },
    {
        "skill": "TensorFlow",
        "priority": "medium",
        "reason": "Required by Machine Learning Engineer. The resume lists Scikit-learn only.",
        "project_name": "Image classifier with Keras",
        "learning_action": "Work through the Keras beginner tutorials, then rebuild one Scikit-learn project.",
        "resource_url": "https://www.tensorflow.org/tutorials",
    },
    {
        "skill": "REST API",
        "priority": "medium",
        "reason": "Required by Backend Developer. Flask is listed but no API work is described.",
        "project_name": "Task tracker API",
        "learning_action": "Build CRUD endpoints with Flask and write tests for each route.",
        "resource_url": "https://flask.palletsprojects.com/",
    },
    {
        "skill": "Power BI",
        "priority": "low",
        "reason": "Preferred by Data Analyst.",
        "project_name": "Sales analytics dashboard",
        "learning_action": "Recreate the internship reports as an interactive dashboard.",
        "resource_url": "https://learn.microsoft.com/power-bi/",
    },
]


def get_resume_analysis() -> dict:
    return deepcopy(_RESUME)


def get_jobs() -> list:
    """List of job_analysis dicts."""
    return deepcopy(_JOBS)


def get_match_results() -> dict:
    """match_result per job, keyed by job title."""
    return deepcopy(_MATCHES)


def get_recommendations() -> list:
    return deepcopy(_RECOMMENDATIONS)

"""Bridge between the UI and src/. Pages call only the functions in this file."""
from ui import mock_data


class ResumeLoadError(Exception):
    """Raised when a resume cannot be used.

    kind is one of: "empty", "unsupported", "corrupted", "text_poor".
    The page turns each kind into a calm explanatory note.
    """

    def __init__(self, kind: str):
        super().__init__(kind)
        self.kind = kind


def load_resume(file) -> dict:
    """Parse an uploaded file and return a resume_analysis dict (see docs/ui_contracts.md).

    `file` is a Streamlit UploadedFile. Raise ResumeLoadError for unusable files.
    """
    name = (getattr(file, "name", "") or "").lower()
    if not name.endswith((".pdf", ".docx")):
        raise ResumeLoadError("unsupported")
    if getattr(file, "size", 1) == 0:
        raise ResumeLoadError("empty")

    # TODO: replace the mock below with the real pipeline.
    #   from src.resume_parser import parse_resume        # bytes -> text (PyMuPDF / python-docx)
    #   from src.skill_extractor import analyse_resume    # text -> sections, skills, keywords
    #   try:
    #       text = parse_resume(file.getvalue(), file.name)
    #   except ValueError:                                 # unreadable or corrupted file
    #       raise ResumeLoadError("corrupted")
    #   if len(text.strip()) < 200:                        # little or no selectable text
    #       raise ResumeLoadError("text_poor")
    #   return analyse_resume(text)                        # must match the resume_analysis shape
    return mock_data.get_resume_analysis()



DEFAULT_WEIGHTS = {"skill": 0.5, "text": 0.3, "experience": 0.2}


def load_job_file(file) -> str:
    """Return the plain text of an uploaded job description (PDF or DOCX).

    Raises ResumeLoadError with kind "empty", "unsupported", "corrupted" or "text_poor".
    """
    name = (getattr(file, "name", "") or "").lower()
    if not name.endswith((".pdf", ".docx")):
        raise ResumeLoadError("unsupported")
    if getattr(file, "size", 1) == 0:
        raise ResumeLoadError("empty")

    # TODO: reuse the text extraction in src/resume_parser.py (same PyMuPDF / python-docx code):
    #   from src.resume_parser import parse_resume
    #   return parse_resume(file.getvalue(), file.name)
    return "Data Analyst. Required: SQL, Python, Pandas, data visualization, Excel. Preferred: Power BI, statistics."


def analyse_job(text: str) -> dict:
    """Analyse job description text and return a job_analysis dict (see docs/ui_contracts.md)."""
    # TODO: replace the mock below with src/job_parser.py, for example:
    #   from src.job_parser import analyse_job as _analyse_job
    #   return _analyse_job(text)
    jobs = mock_data.get_jobs()
    lowered = (text or "").lower()
    for job in jobs:
        if job["title"].lower() in lowered:
            return job
    return jobs[0]


def score_match(resume_analysis: dict, job_analysis: dict, weights: dict | None = None) -> dict:
    """Compare a resume with a job and return a match_result dict (see docs/ui_contracts.md).

    weights is {"skill": float, "text": float, "experience": float} and should sum to 1.
    """
    weights = dict(weights or DEFAULT_WEIGHTS)

    # TODO: replace the mock below with src/similarity_engine.py and src/match_scorer.py, for example:
    #   from src.match_scorer import score_match as _score_match
    #   return _score_match(resume_analysis, job_analysis, weights=weights)
    results = mock_data.get_match_results()
    result = results.get(job_analysis["title"]) or next(iter(results.values()))
    c = result["components"]
    skill = 0.7 * c["required_skill_coverage"] + 0.3 * c["preferred_skill_coverage"]
    result["overall"] = round(
        weights["skill"] * skill + weights["text"] * c["text_similarity"] + weights["experience"] * c["experience_relevance"],
        1,
    )
    result["weights"] = weights
    return result


# TODO: replace with the category column of data/skills.csv (your skill taxonomy).
_MOCK_CATEGORIES = {
    "Python": "Programming", "SQL": "Programming", "Docker": "Cloud/DevOps", "AWS": "Cloud/DevOps",
    "MLOps": "Cloud/DevOps", "TensorFlow": "Machine Learning", "PyTorch": "Machine Learning",
    "Scikit-learn": "Machine Learning", "Statistics": "Machine Learning", "Excel": "Data",
    "Power BI": "Data", "Tableau": "Data", "Data Visualization": "Data", "Pandas": "Data",
    "REST API": "Web/Backend", "Flask": "Web/Backend", "PostgreSQL": "Web/Backend", "Redis": "Web/Backend",
}


def skill_category(skill: str) -> str:
    """Return the taxonomy category for a skill, or "Other" if unknown."""
    return _MOCK_CATEGORIES.get(skill, "Other")


def get_recommendations(missing_skills: list, jobs: list) -> list:
    """Return the recommendations contract (see docs/ui_contracts.md) for the given gaps.

    missing_skills: skills missing from the resume. jobs: list of job_analysis dicts
    (used to see how often, and how strongly, each skill is requested).
    """
    # TODO: replace the mock below with src/recommendations.py, for example:
    #   from src.recommendations import get_recommendations as _get_recommendations
    #   return _get_recommendations(missing_skills, jobs)
    curated = {r["skill"].lower(): r for r in mock_data.get_recommendations()}
    required = {s.lower() for j in jobs for s in j["required_skills"]}
    recs = []
    for skill in dict.fromkeys(missing_skills):
        rec = curated.get(skill.lower())
        if rec is None:
            rec = {
                "skill": skill,
                "priority": "medium" if skill.lower() in required else "low",
                "reason": f"{skill} is requested in the jobs you are targeting and was not found in the resume.",
                "project_name": f"Small {skill} project",
                "learning_action": f"Work through an introductory {skill} tutorial, then apply it in a small project.",
                "resource_url": "https://www.google.com/search?q=" + skill.replace(" ", "+") + "+tutorial",
            }
        recs.append(rec)
    return recs

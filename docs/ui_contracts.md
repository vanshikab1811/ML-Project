# ResumeIQ UI contracts

The UI consumes only these shapes. `ui/mock_data.py` returns them today; `src/` modules must return the same shapes.

```python
resume_analysis = {
    "text": str,
    "sections": {"summary": bool, "education": bool, "experience": bool,
                 "projects": bool, "skills": bool, "certifications": bool},
    "skills_by_category": {category: [skill, ...]},
    "keywords": [{"term": str, "section": str, "snippet": str}],
}

job_analysis = {
    "title": str,
    "required_skills": [..],
    "preferred_skills": [..],
    "responsibilities": [..],
    "keywords": [..],
    "experience_terms": [..],
}

match_result = {
    "overall": float,  # 0-100
    "components": {
        "required_skill_coverage": float,
        "preferred_skill_coverage": float,
        "text_similarity": float,
        "keyword_coverage": float,
        "experience_relevance": float,
    },  # each 0-100
    "weights": {"skill": 0.5, "text": 0.3, "experience": 0.2},
    "matched": [..],
    "missing_required": [..],
    "missing_preferred": [..],
    "extra": [..],
    "explanation": str,
}

recommendations = [
    {"skill": str, "priority": "high" | "medium" | "low", "reason": str,
     "project_name": str, "learning_action": str, "resource_url": str}
]
```

## Mock data accessors (`ui/mock_data.py`)

| Function | Returns |
|---|---|
| `get_resume_analysis()` | one `resume_analysis` |
| `get_jobs()` | list of `job_analysis` |
| `get_match_results()` | dict of `match_result` keyed by job title |
| `get_recommendations()` | `recommendations` list |


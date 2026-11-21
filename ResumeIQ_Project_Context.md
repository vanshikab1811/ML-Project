# ResumeIQ --- Project Context & Master Brief

## 1. Project identity

**Project title:** ResumeIQ: An Intelligent Resume Analysis, Job
Matching and Skill Gap Recommendation System Using Natural Language
Processing and Machine Learning

**Project type:** Individual Machine Learning course project / working
software application

**Student context:** Third-year CS student building an individual ML
project. The project should be substantial enough to demonstrate genuine
ML learning and experimentation, but feasible at an intermediate level
and not unnecessarily research-heavy.

**Chosen idea:** Resume Analyzer and Job-Matching Application.

## 2. Problem statement

Students and job seekers often do not know how closely their resume
aligns with a particular job description, which important skills they
are missing or under-representing, or what they should learn or build to
improve their fit for roles they want.

ResumeIQ will accept a resume and one or more job descriptions, process
and analyse their text, extract skills and important keywords, estimate
resume-to-job compatibility, identify skill gaps, recommend learning
actions/projects, and allow users to compare job opportunities against
the same resume.

The app is an assistive analysis tool. A compatibility score is an
**estimated resume-to-job alignment score**, not a hiring probability,
guarantee of an interview, or prediction that a person will get hired.

## 3. Main product goal

Do not build only a resume checker that returns one percentage. Build an
explainable, useful application that answers:

1.  What skills and relevant information does the resume contain?
2.  What does the job description ask for?
3.  Which requirements appear to match?
4.  Which requirements appear missing or underrepresented?
5.  Why was the compatibility score calculated?
6.  What practical skills, topics, learning resources, or projects could
    help address gaps?
7.  Which of several job descriptions appears to align most closely with
    this resume?

## 4. Core user workflow

1.  User opens ResumeIQ.
2.  Uploads a resume (PDF or DOCX).
3.  App extracts the text and presents it for review so the user can
    spot parsing errors.
4.  App analyses the resume: sections, skills, skill categories,
    keywords, and completeness indicators.
5.  User pastes or uploads a job description, or selects a previously
    saved job description.
6.  App analyses the job: title if identifiable, requirements,
    required/preferred skills, keywords, responsibilities, and
    experience/education terms.
7.  Matching engine compares the resume and job description.
8.  Results dashboard shows a compatibility estimate and its components,
    matches, gaps, strengths, and explanation.
9.  App recommends priorities, learning topics, and relevant projects.
10. User can compare the same resume against multiple jobs.
11. Optionally, analyses are saved to history and can be revisited or
    compared after resume updates.

## 5. Feature scope

### 5.1 Resume upload and parsing --- core

-   Accept PDF and DOCX.
-   Extract text.
-   Handle empty, corrupted, unsupported, or text-poor files gracefully.
-   Display extracted text for verification.
-   Identify common resume sections when feasible: summary/objective,
    education, experience, projects, skills, certifications.
-   Extract contact details only if needed for parsing/completeness;
    avoid unnecessary display or retention of personal information.
-   Scanned/image-only PDFs may not yield text from ordinary extraction.
    OCR is an optional future enhancement, not a requirement for the
    first version.

**Libraries:** PyMuPDF for PDF text extraction; python-docx for DOCX
text extraction.

### 5.2 Resume intelligence and skill extraction --- core

-   Extract technical skills and relevant keywords.
-   Categorize skills, for example:
    -   Programming: Python, Java, C++, JavaScript
    -   Machine Learning: ML, Scikit-learn, TensorFlow, PyTorch, NLP,
        regression, classification
    -   Data: SQL, Pandas, NumPy, Power BI
    -   Web/Backend: React, Node.js, Flask, Django, REST API
    -   Cloud/DevOps: AWS, Azure, Docker, Kubernetes
-   Normalize skill names and aliases (e.g., `sklearn` → `Scikit-learn`,
    `reactjs` → `React`).
-   Handle phrase matching, case, punctuation, duplicates, and common
    variations.
-   Show extracted skills grouped by category.
-   Show keywords and, where feasible, where they were found (resume
    section/snippet).
-   Provide a simple completeness/structure analysis; do not claim a
    validated ATS score.

**Implementation approach:** Begin with a curated skill taxonomy/alias
file and rule/dictionary matching with preprocessing. This is
transparent, manageable, and testable. Add NLP or fuzzy/semantic
matching later only if it adds value and can be evaluated.

### 5.3 Job description analysis --- core

Input methods: - Paste job-description text. - Upload PDF/DOCX. -
Optionally save a job description for reuse.

Extract/identify: - Job title, if possible. - Required skills. -
Preferred/nice-to-have skills. - Keywords and phrases. -
Responsibilities. - Experience and education terms, if present.

For the first implementation, required/preferred detection can use
patterns and contextual keywords such as "required," "must have,"
"preferred," "bonus," and "nice to have," combined with the skill
taxonomy. Avoid overclaiming perfect extraction.

### 5.4 Resume--job matching engine --- core

Produce several components instead of an unexplained single score:

-   Required-skill coverage.
-   Preferred-skill coverage.
-   Resume/job text similarity.
-   Project/experience relevance (initially a heuristic if no labelled
    data supports a trained model).
-   Keyword coverage.

Possible initial score formula (heuristic and configurable; not a
scientifically established hiring formula):

`Match Score = 0.50 × Skill Match + 0.30 × Text Similarity + 0.20 × Experience/Project Relevance`

All component scores must be on a consistent 0--100 scale before
combining. Document the weights and make them adjustable during
experiments. Label the overall result clearly as an estimate of document
alignment.

Skill match should distinguish: - Matched skills. - Missing required
skills. - Missing preferred skills. - Additional skills in resume. -
Related/alias matches where appropriate.

### 5.5 Text similarity --- core ML/NLP component

-   Text preprocessing.
-   TF-IDF vectorization.
-   Cosine similarity.
-   Experiment with choices such as unigram vs. unigram/bigram,
    stop-word handling, whole-document vs. section-specific comparisons.
-   Explain that TF-IDF similarity measures textual overlap/relevance,
    not competence or hiring outcome.

**Library:** Scikit-learn (`TfidfVectorizer`, cosine similarity
utilities).

### 5.6 Skill-gap analysis --- core

-   Show missing or underrepresented requirements.
-   Distinguish required from preferred where the extraction can support
    it.
-   Prioritize gaps using a transparent rule/heuristic based on
    requirement type, frequency across target jobs, and relevance.
-   When comparing several jobs, identify skills repeatedly requested
    across the user's target roles.

### 5.7 Recommendations --- core

Use a curated project/learning recommendation database, initially a CSV.

Example: - SQL → Sales Analytics Dashboard, Customer Segmentation,
database project - Machine Learning → Churn Prediction, Recommendation
System, regression/classification project - NLP → Text Classification,
Sentiment Analysis, Resume Keyword Extractor

Recommend: - Learning topics. - Practice actions. - Projects that cover
missing skills. - Suggested priority and explanation.

Recommendations should be explainable and based on detected gaps, not
pretend to be a sophisticated learned recommender unless a model is
later trained and evaluated.

### 5.8 Multiple-job comparison --- core

-   Analyse one resume against multiple job descriptions.
-   Rank jobs by estimated alignment.
-   Show score breakdown per job.
-   Compare matched and missing skills.
-   Identify common skills across job descriptions and high-priority
    gaps.
-   Allow sorting/filtering.

### 5.9 Dashboard --- core

Suggested visualizations: - Overall compatibility estimate. - Skill
coverage donut/bar chart. - Component score breakdown. - Matched
vs. missing skills. - Missing skills by category. - Job comparison
ranking. - Commonly requested skills across saved jobs.

### 5.10 History and storage --- optional / stretch

-   Save analyses and job descriptions.
-   Track analyses over time or compare after a resume update.
-   Use SQLite.
-   Avoid storing sensitive resume data by default without clear user
    consent; provide a way to remove stored records.

### 5.11 PDF report export --- optional / stretch

-   Export analysis summary, score breakdown, skills, gaps, and
    recommendations.
-   Only add if time permits.

## 6. Technology stack (recommended)

Keep the first implementation Python-based; avoid a separate React
frontend or complicated backend unless the scope later requires it.

-   **Language:** Python
-   **UI/application:** Streamlit
-   **ML:** Scikit-learn
-   **NLP:** NLTK and/or spaCy (use only components actually needed; do
    not add both just for the sake of it)
-   **PDF text extraction:** PyMuPDF
-   **DOCX text extraction:** python-docx
-   **Data manipulation:** Pandas, NumPy
-   **Charts:** Plotly
-   **Database:** SQLite (optional core persistence; can be added after
    basic app works)
-   **Model serialization:** Joblib, if trained models need to be saved
-   **Development:** VS Code and Jupyter Notebook
-   **Version control:** Git and GitHub

### Why this stack

Streamlit allows a multi-page Python UI with upload controls, charts,
tables, and interactive dashboards. Scikit-learn provides vectorization,
similarity, preprocessing, classifiers, evaluation, and other ML tools.
PyMuPDF and python-docx extract document text. Plotly supports
interactive visualizations. SQLite can store analysis history.

## 7. ML/NLP components and learning objectives

The project should demonstrate understanding of the following rather
than merely call APIs:

1.  Text extraction and data quality.
2.  Text preprocessing (case normalization, tokenization as appropriate,
    punctuation/whitespace handling, stop words; consider
    stemming/lemmatization only if useful).
3.  Skill taxonomy, phrase matching, alias normalization, and
    limitations of dictionary-based extraction.
4.  TF-IDF: vocabulary, term frequency, inverse document frequency,
    sparse vectors.
5.  Cosine similarity and its interpretation.
6.  Feature engineering from resume/job pairs:
    -   required skill coverage
    -   preferred skill coverage
    -   keyword coverage
    -   TF-IDF similarity
    -   project/experience relevance (initially carefully defined
        heuristic)
7.  Transparent score construction and weight experiments.
8.  Optional supervised classification of resume--job pairs
    (Strong/Moderate/Weak) if sufficient trustworthy labels can be
    obtained.
9.  Model evaluation and error analysis.
10. Optional semantic embeddings comparison with TF-IDF as an advanced
    extension.

## 8. Planned experiments (for course/report depth)

Conduct experiments rather than just build features:

### Experiment 1: Text preprocessing variants

Compare, where appropriate: - Minimal cleaning vs. more preprocessing. -
Unigrams vs. unigram/bigram features. - Whole-document vs. selected
resume sections.

Evaluate similarity/ranking against manually reviewed examples.

### Experiment 2: Skill extraction quality

Create a manually annotated sample of resumes and compare extractor
results: - Precision - Recall - F1-score

### Experiment 3: Similarity/ranking quality

Create a small, human-reviewed set of resume--job pairs and relevance
labels or rankings (e.g., high, medium, low alignment). Assess whether
the system ranks examples sensibly. Depending on data/labels, use
Spearman rank correlation, Precision@K, or Mean Reciprocal Rank where
appropriate.

### Experiment 4: Score weights

Try different component weights for skill coverage, text similarity, and
experience/project relevance. Explain how results change. Do not claim
weights are objectively optimal without suitable validation.

### Experiment 5: Optional classifier

If enough labelled resume--job pairs are available: - Build features
from the components above. - Compare Logistic Regression, Decision Tree,
and Random Forest. - Use train/validation/test splits and avoid
leakage. - Report Accuracy, Precision, Recall, F1, and confusion
matrix. - If labels are imbalanced, use appropriate metrics and consider
class weighting. - Synthetic or heuristic labels must be clearly
identified and cannot establish real-world validity.

### Experiment 6: Optional semantic similarity

Compare TF-IDF/cosine similarity with a pretrained sentence-embedding
model. This is an extension only; it may introduce heavier dependencies
and should be kept if it can be evaluated and explained.

## 9. Dataset strategy

The project needs several data sources/types:

### Resume examples

-   Public resume datasets, if license/usage permits.
-   Fictional/sample resumes created for testing.
-   User-provided resumes only with permission and appropriate handling.
-   A manually annotated subset for extraction evaluation.

### Job descriptions

-   Public job-description datasets, subject to their terms.
-   Sample descriptions authored for controlled tests.
-   Job postings gathered in accordance with site terms and dataset
    licences.
-   Do not make real-time scraping a project dependency.

### Skill taxonomy

Maintain an editable CSV containing: - canonical skill - category -
aliases - optionally related skills - optionally priority or metadata

Example columns: `skill,category,aliases`

Example: `Scikit-learn,Machine Learning,sklearn|scikit learn`

### Recommendation database

Curated CSV, for example:
`skill,project_name,description,learning_action,resource_url,priority`

### Evaluation set

Create manually reviewed resume--job pairs with clear criteria and
labels. Separate the evaluation set from any data used to tune weights
or train a classifier.

**Data integrity:** Do not claim that synthetic labels or simulated data
represent hiring outcomes. Make dataset provenance, limitations, and
annotation process explicit.

## 10. Score design (initial plan; subject to experiments)

Possible components: - `S`: skill coverage, 0--100. - `T`: TF-IDF text
similarity scaled to 0--100. - `E`: experience/project relevance, 0--100
(initially heuristic unless validated labels/model support it).

Initial formula: `Score = 0.50*S + 0.30*T + 0.20*E`

Potential refinements: - Calculate required and preferred skill coverage
separately. - Weight required skills more than preferred skills. - Avoid
double-counting a skill/keyword excessively. - Explain every
component. - Allow the formula/weights to be tested and adjusted. - Do
not label the score as ATS score or hiring probability unless that is
truly measured (it is not).

## 11. Proposed UI/pages

Streamlit multi-page app:

1.  **Dashboard**
    -   Recent analyses.
    -   Number of resumes/jobs analysed (if history exists).
    -   Average estimated match (descriptive only).
    -   Common skill gaps.
    -   Skills distribution.
2.  **Resume Analysis**
    -   Upload PDF/DOCX.
    -   Show extracted text for verification.
    -   Skills by category, keywords, sections/completeness.
3.  **Job Match**
    -   Select/upload resume.
    -   Paste/upload job description.
    -   Match score and component breakdown.
    -   Matched/missing/extra skills.
    -   Strengths and explanations.
4.  **Compare Jobs**
    -   Resume once; multiple job descriptions.
    -   Ranked results, score components, common skill gaps.
5.  **Skill Gap & Learning Roadmap**
    -   Prioritized missing skills.
    -   Learning actions and project suggestions.
    -   Optional roadmap based on target jobs.
6.  **History** (optional)
    -   Saved results, past job descriptions, resume-version
        comparisons.

## 12. UI style

Target a clean, professional, modern SaaS-like interface. Suggested
palette: white/light background with navy and restrained blue/purple
accents, or a consistent dark theme. Keep charts readable and
uncluttered.

Results-page layout: - Top: resume/job title and estimated
compatibility. - Middle: component scores, skill coverage, strengths. -
Bottom: missing skills, priorities, recommended projects/learning. -
Multiple-job comparison: sortable ranked table and comparison charts.

Design should not be overly decorative; clarity and usability matter.

## 13. Architecture / folder structure (proposed)

``` text
ResumeIQ/
├── app.py
├── requirements.txt
├── README.md
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Resume_Analysis.py
│   ├── 3_Job_Match.py
│   ├── 4_Compare_Jobs.py
│   ├── 5_Learning_Roadmap.py
│   └── 6_History.py
├── src/
│   ├── resume_parser.py
│   ├── job_parser.py
│   ├── text_preprocessing.py
│   ├── skill_extractor.py
│   ├── keyword_extractor.py
│   ├── similarity_engine.py
│   ├── match_scorer.py
│   ├── classifier.py
│   ├── recommendations.py
│   └── evaluation.py
├── data/
│   ├── skills.csv
│   ├── skill_aliases.csv (or aliases integrated in skills.csv)
│   ├── project_recommendations.csv
│   ├── sample_resumes/
│   └── sample_jobs/
├── models/
│   └── trained_model.pkl (only if a model is trained and saved)
├── database/
│   └── resumeiq.db (if SQLite persistence is implemented)
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_text_preprocessing.ipynb
│   ├── 03_skill_extraction.ipynb
│   ├── 04_similarity_experiments.ipynb
│   └── 05_model_evaluation.ipynb
└── tests/
    ├── test_parser.py
    ├── test_skills.py
    └── test_matching.py
```

Structure can be simplified or changed as implementation evolves. Do not
create every file at the beginning; build incrementally.

## 14. Development phases

### Phase 1 --- Setup and document processing

-   Confirm Python version and IDE.
-   Create project directory and virtual environment.
-   Install dependencies.
-   Start Streamlit app.
-   Upload PDF/DOCX and extract text.
-   Handle errors and show extracted text.

### Phase 2 --- Dataset exploration and NLP

-   Locate suitable datasets; inspect licences and formats.
-   Explore resume/job text.
-   Clean text.
-   Build taxonomy and aliases.
-   Implement skill extraction and category display.
-   Test extraction manually.

### Phase 3 --- Baseline matching engine

-   Extract job skills and resume skills.
-   Calculate required/preferred skill coverage.
-   TF-IDF vectorization.
-   Cosine similarity.
-   Implement transparent score breakdown.
-   Test with manually designed cases.

### Phase 4 --- Gaps and recommendations

-   Missing-skill identification.
-   Priority scoring.
-   Curated learning/project recommendation mapping.
-   Explain recommendations.

### Phase 5 --- Multiple job comparisons

-   Reuse a parsed resume.
-   Analyse multiple job descriptions.
-   Rank and compare.
-   Find common skill requirements and gaps.

### Phase 6 --- Experiments and evaluation

-   Annotate a small evaluation dataset.
-   Evaluate skill extraction.
-   Evaluate similarity/ranking.
-   Compare preprocessing choices.
-   Test score weights.
-   Optional classifier, if enough credible labels.

### Phase 7 --- UI polish, storage and testing

-   Dashboard and charts.
-   Optional SQLite history.
-   Optional PDF report.
-   End-to-end tests.
-   README and screenshots.

### Phase 8 --- Academic deliverables

-   Project report.
-   Problem statement, objectives, scope.
-   Literature/background research if required.
-   Methodology and system architecture.
-   Dataset description and limitations.
-   Experiments, metrics, results.
-   Error analysis.
-   Future work.
-   Presentation/demo script and viva preparation.

## 15. Suggested schedule (rough)

A 5--7 week plan, adjusted to deadline and workload:

-   Week 1: Dataset exploration and setup.
-   Week 2: Parsing, preprocessing, skill extraction.
-   Week 3: TF-IDF, cosine similarity, baseline matching.
-   Week 4: Skill-gap analysis and recommendations.
-   Week 5: Multi-job comparison and UI.
-   Week 6: ML experiments, evaluation, testing.
-   Week 7: Polish, report, demo, presentation.

This is only a planning estimate. Prioritize a working end-to-end core
over optional features.

## 16. Final scope decisions

### Must-have

-   PDF/DOCX resume upload.
-   Job description paste/upload.
-   Text extraction and verification.
-   Skill extraction and categorization.
-   TF-IDF and cosine similarity.
-   Transparent compatibility score and components.
-   Matched and missing skills.
-   Skill gap analysis.
-   Learning/project recommendations.
-   Multiple job comparison.
-   Dashboard visualizations.
-   Proper experiments and evaluation.

### Nice-to-have / stretch

-   Supervised match classifier.
-   Semantic sentence embeddings.
-   OCR for scanned resumes.
-   Resume section detection beyond basic heuristics.
-   Resume quality/completeness insights.
-   SQLite history.
-   Resume-version comparison.
-   PDF export.
-   User feedback loop.

Do not allow stretch goals to delay the core working application.

## 17. Testing and quality requirements

Test at least: - Valid PDF. - Valid DOCX. - Empty/corrupted file. - PDF
with little/no selectable text. - Resume with skills expressed as
aliases. - Skills mentioned in different case/punctuation. - Duplicate
skills. - Job description with required/preferred phrases. - Resume with
no obvious skills. - Job description with no skill terms. - Several job
descriptions in comparison. - Match score component values are within
expected ranges. - Score explanation is consistent with detected
skills. - No false claim that score predicts hiring.

Use modular code and functions; keep ML logic outside UI page files.

## 18. Responsible use, privacy and limitations

-   Resume files contain personal information. Minimize collection and
    retention.
-   Prefer local processing for the prototype where practical.
-   If analysis history is saved, explain it and provide deletion
    controls.
-   Do not store contact information unnecessarily.
-   Compatibility scores are estimates and can be biased by wording,
    keyword matching, incomplete taxonomies, and resume formatting.
-   A missing keyword does not prove the person lacks the skill.
-   Related/transferable skills may be missed.
-   Skill extraction can make false positives and false negatives.
-   Text similarity does not measure actual competence.
-   The tool must not be presented as predicting hiring success or
    replacing human judgement.
-   Make the score calculation and recommendations explainable.

## 19. What to explain in a viva

Be ready to explain: - Why TF-IDF is used. - How TF-IDF differs from raw
word counts. - What cosine similarity measures. - Why similarity is not
the same as a true match. - How skills are extracted and normalized. -
Precision, recall and F1 for extraction. - How feature engineering is
performed. - How the score formula was chosen and limitations of
heuristic weights. - How the classifier works, if included. - Train/test
split, cross-validation, leakage, overfitting. - Why accuracy can be
misleading with class imbalance. - Data provenance and annotation. -
Errors, limitations, fairness and privacy. - Why this system cannot
predict whether someone will be hired.

## 20. Collaboration style and student learning preferences

-   The student wants to learn the ML deeply, not merely receive a
    finished code dump.
-   Work step-by-step, explaining concepts in beginner-friendly language
    while maintaining intermediate project depth.
-   Start with the data and notebook experiments before integrating the
    app.
-   Provide complete runnable code for each stage, with clear filenames,
    setup instructions, and explanation.
-   Avoid overwhelming the student with all modules at once.
-   Explain why each technology and algorithm is used and what
    alternatives were considered.
-   Make sure each milestone works before moving on.
-   Use practical examples and test cases.
-   Keep the project feasible for one student and avoid unnecessary
    advanced research or infrastructure.
-   When debugging, explain the cause and provide a corrected complete
    implementation of the relevant file/module when appropriate.

## 21. Immediate next steps

1.  Confirm deadline, expected submission format, and any course
    restrictions (if not yet known).
2.  Settle on a dataset strategy and locate/inspect candidate datasets
    before committing.
3.  Create project directory and environment.
4.  Begin with a data exploration notebook.
5.  Establish a baseline skill taxonomy and test examples.
6.  Build the first working end-to-end pipeline: upload → parse →
    extract skills → analyse one job → show results.
7.  Add and evaluate more advanced ML components after the baseline
    works.

## 22. One-paragraph project summary

ResumeIQ is a Python-based application that analyses resumes and job
descriptions using NLP and machine learning. It extracts and categorizes
skills, represents text with TF-IDF, measures similarity using cosine
similarity, calculates an explainable resume-to-job alignment estimate,
identifies skill gaps, recommends learning actions and projects, and
compares a single resume against multiple job opportunities. It is built
with Streamlit, Scikit-learn, PyMuPDF, python-docx, Pandas, NumPy,
Plotly, and optionally SQLite. The project includes experiments and
evaluation for skill extraction and similarity/ranking, with an optional
supervised compatibility classifier if a sufficiently reliable labelled
dataset is available. The score is explicitly an estimate of
textual/skill alignment, not a hiring prediction.

## 23. Dataset links and download recommendations

These dataset links were shortlisted for ResumeIQ. Start with the two primary datasets below; download other datasets only if they become useful for a specific experiment. Check each dataset's licence, terms, availability, format, and provenance before use.

### Primary datasets — recommended starting point

1. **Resume Dataset — Sneha Bhawal (Kaggle)**
   - Link: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
   - Intended use: resume text exploration, NLP preprocessing, skill extraction development, and resume-category classification experiments.
   - Reported in the shortlist as approximately 2,484 resumes across categories; verify the current dataset contents after download.

2. **Job Description Dataset — Ravindra Singh (Kaggle)**
   - Link: https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset
   - Intended use: job-description parsing, keyword/skill extraction, and test data for resume–job matching. Inspect the actual columns and contents before finalizing use.

### Supplementary datasets

3. **Resume Dataset — Gaurav Dutta (Kaggle)**
   - Link: https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset
   - Intended use: supplementary resume text/category data for NLP and classification.

4. **Updated Resume Dataset (Kaggle)**
   - Link: https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset
   - Intended use: alternative resume corpus; shortlist description reported 962 resumes across 25 categories (verify on download).

5. **LinkedIn Job Postings Dataset (Kaggle)**
   - Link: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
   - Intended use: larger job-posting corpus and job comparison experiments. May be larger than needed for the first prototype.

6. **Jobs on Naukri.com (Kaggle / PromptCloud)**
   - Link: https://www.kaggle.com/datasets/PromptCloudHQ/jobs-on-naukricom
   - Intended use: optional India-focused job-description data. Check dataset terms and whether its content fits our roles.

7. **Resume–Job Fit Dataset (Hugging Face)**
   - Link: https://huggingface.co/datasets/batuhanmtl/job_resume_fit
   - Intended use: supplementary resume/job pair exploration and matching experiments. The shortlist described 2,385 pairs with skills/categories and matching scores; inspect how scores/labels were produced. Generated or heuristic scores must not be treated as verified hiring outcomes.

8. **Job Skill Set Dataset (Hugging Face)**
   - Link: https://huggingface.co/datasets/batuhanmtl/job-skill-set
   - Intended use: job skill extraction and validation; shortlist description reported 1,167 job postings with titles, descriptions, categories, and skill sets (verify current dataset details).

9. **CareerCorpus — Annotated Resume Dataset (Mendeley Data)**
   - Link: https://data.mendeley.com/datasets/wzzwn37gmd
   - Intended use: supplementary resume classification and annotation-based evaluation. Shortlist description reported 302 annotated resumes across six occupational categories; verify availability and documentation.

### Dataset selection plan

- Begin with **Resume Dataset — Sneha Bhawal** and **Job Description Dataset — Ravindra Singh** only.
- Preserve original downloaded files; work from copies.
- In the first data-exploration notebook, record file names, formats, columns, row counts, missing values, duplicates, text lengths, category distributions, and any licensing/provenance notes.
- Choose supplementary datasets only after identifying a concrete gap (e.g., resume–job pairs for ranking evaluation or job skills for extractor testing).
- Do not assume a dataset's reported size, labels, or fields without checking the downloaded version.
- Avoid making live scraping of job sites a dependency for the project.
- Treat synthetic, automatically generated, or heuristic matching labels as weak/supplementary evidence; disclose their origin and do not claim they represent real hiring decisions.

### Dataset links quick list

- Primary resume dataset: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
- Primary job description dataset: https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset
- Supplementary resume dataset: https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset
- Updated resumes: https://www.kaggle.com/datasets/jillanisofttech/updated-resume-dataset
- LinkedIn postings: https://www.kaggle.com/datasets/arshkon/linkedin-job-postings
- Naukri postings: https://www.kaggle.com/datasets/PromptCloudHQ/jobs-on-naukricom
- Resume–job fit: https://huggingface.co/datasets/batuhanmtl/job_resume_fit
- Job skill set: https://huggingface.co/datasets/batuhanmtl/job-skill-set
- CareerCorpus: https://data.mendeley.com/datasets/wzzwn37gmd


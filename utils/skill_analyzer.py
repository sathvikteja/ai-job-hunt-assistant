from sentence_transformers import SentenceTransformer, util

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

SKILLS = [

    # Programming
    "python","r","java","c++","scala","matlab",

    # Data science
    "data analysis","data analytics","data science",
    "statistics","probability","linear algebra",
    "data visualization",

    # ML / AI
    "machine learning","deep learning","artificial intelligence",
    "natural language processing","computer vision",
    "reinforcement learning","time series forecasting",
    "recommendation systems",

    # ML libraries
    "scikit-learn","pytorch","tensorflow","keras",
    "xgboost","lightgbm","catboost",

    # Python libraries
    "pandas","numpy","matplotlib","seaborn",
    "plotly","scipy",

    # NLP tools
    "spacy","nltk","transformers","bert","huggingface",

    # Data engineering
    "sql","postgresql","mysql","mongodb",
    "spark","hadoop","airflow","kafka",

    # Cloud
    "aws","azure","google cloud","gcp",

    # MLOps
    "docker","kubernetes","mlflow","dvc","kubeflow",

    # Big data
    "pyspark","databricks",

    # BI tools
    "tableau","power bi","looker",

    # Deployment
    "fastapi","flask","streamlit",

    # Version control
    "git","github",

    # Experimentation
    "a/b testing","feature engineering","model deployment",
]


def extract_skills_semantic(text, threshold=0.35):

    text_embedding = model.encode(text, convert_to_tensor=True)

    detected_skills = []

    for skill in SKILLS:

        skill_embedding = model.encode(skill, convert_to_tensor=True)

        score = util.cos_sim(text_embedding, skill_embedding).item()

        if score > threshold:
            detected_skills.append(skill)

    return list(set(detected_skills))


def skill_gap_analysis(resume_text, job_text):

    resume_skills = extract_skills_semantic(resume_text)
    job_skills = extract_skills_semantic(job_text)

    matching = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    return matching, missing
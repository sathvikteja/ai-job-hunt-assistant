# 🤖 AI Job Hunt Assistant

An **AI-powered job search assistant** that automatically recommends relevant jobs, analyzes skill gaps, and generates personalized application materials using **multi-agent AI and semantic similarity models**.

The system helps candidates **discover suitable jobs, understand missing skills, and generate professional outreach messages** using AI.

---

# 🚀 Features

### 🔎 Semantic Job Recommendation

Jobs are ranked using **sentence embeddings and cosine similarity** between the user's resume and job descriptions.

### 🧠 Skill Gap Analysis

The system automatically detects:

* Matching skills between resume and job
* Missing skills required for the role

### 🤖 AI Agent Pipeline

AI agents collaborate to:

* Analyze job descriptions
* Generate tailored resume summaries
* Write cover letters
* Create outreach messages to hiring managers

### 📊 Intelligent Job Ranking

Jobs are ranked based on **semantic similarity scores**, allowing more accurate recommendations than simple keyword matching.

### 🖥 Interactive UI

A **Streamlit interface** allows users to:

* Enter job search parameters
* Upload or paste resumes
* View recommended jobs
* Analyze skill gaps
* Generate application materials

---

# 🧠 System Architecture

```
Resume
  ↓
Sentence Embeddings (SentenceTransformers)
  ↓
Cosine Similarity Matching
  ↓
Job Ranking
  ↓
Skill Gap Analysis
  ↓
AI Agent Pipeline (CrewAI)
  ↓
Generated Outputs
   ├── Resume Summary
   ├── Cover Letter
   └── Outreach Message
---

---

## 🧩 Project Structure

```
ai-job-hunt-assistant
│
├── 🤖 agents
│   ├── jd_analyst.py
│   ├── resume_cl_agent.py
│   └── messaging_agent.py
│
├── 🧠 utils
│   ├── embeddings.py
│   ├── job_matcher.py
│   ├── skill_analyzer.py
│   ├── config.py
│   └── tracking.py
│
├── 📂 data
│   ├── sample_resume.txt
│   ├── outreach_message.txt
│   └── report.md
│
├── 🖥 streamlit_app.py
├── ⚙ orchestrator.py
├── 🌐 usajobs_api.py
├── 📦 requirements.txt
└── 📘 README.md
```
---

# 🧠 Technologies Used

### Machine Learning / NLP

* Sentence Transformers
* Semantic Embeddings
* Cosine Similarity
* Skill Extraction

### AI Frameworks

* CrewAI (multi-agent system)
* LLMs for content generation

### Backend

* Python
* REST APIs
* USAJobs API

### Frontend

* Streamlit

### Libraries

* sentence-transformers
* scikit-learn
* numpy
* pandas

---

# 📊 How Job Recommendation Works

1. User enters resume and job keyword
2. System fetches jobs using the **USAJobs API**
3. Job descriptions are converted to **embeddings**
4. Resume is converted to **embedding vector**
5. Cosine similarity calculates job relevance
6. Jobs are ranked based on match score

---

# 🧠 Skill Gap Analysis

The system extracts skills from:

* Resume
* Job description

Then it identifies:

Matching Skills = Resume ∩ Job Skills
Missing Skills = Job Skills − Resume Skills

This helps candidates understand **what skills they need to improve to qualify for the job**.

---

# 🤖 AI Generated Outputs

The AI pipeline generates:

### Resume Summary

Tailored summary based on the job description.

### Cover Letter

Automatically generated cover letter aligned with the role.

### Outreach Message

Professional message to contact hiring managers.

Example:

Dear Hiring Manager,

I am excited to express my interest in the Data Scientist position.
With experience in machine learning, NLP, and data analysis,
I believe my skills align well with the requirements of the role.

I would welcome the opportunity to discuss how my experience
can contribute to your team.

Best regards,
Sathvik

---

# 🖥 Application Interface

### Home Page

![Home](screenshots/home_page_ui.png)

### Job Recommendations

![Jobs](screenshots/recommended_jobs.png)

### Skill Gap Analysis

![Skills](screenshots/skill_gap_analysis.png)

### AI Generated Outreach Message

![AI Output](screenshots/ai_outreach_message.png)

---

# ⚙ Installation

Clone the repository:

git clone https://github.com/sathvikteja/ai-job-hunt-assistant.git

cd ai-job-hunt-assistant

Install dependencies:

pip install -r requirements.txt

---

# ▶ Run the Application

streamlit run streamlit_app.py

The app will start at:

http://localhost:8502

---

# 📈 Future Improvements

* RAG-based job knowledge retrieval
* Vector database for job storage
* Resume auto-optimization
* Skill ontology graph
* Personalized job alerts

---

# 👨‍💻 Author

Sathvik Teja

Interested in:

* Artificial Intelligence
* Machine Learning
* NLP
* Recommendation Systems

---

This project demonstrates how **semantic search, AI agents, and NLP can automate and improve the job application process.**

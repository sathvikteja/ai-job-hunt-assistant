import streamlit as st

from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline
from utils.job_matcher import compute_similarity
from utils.skill_analyzer import skill_gap_analysis


st.set_page_config(
    page_title="AI Job Hunt Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Job Hunt Assistant")

st.markdown("""
This app uses AI agents to help with your job search.

The system will:

• Recommend jobs using semantic similarity  
• Analyze job descriptions  
• Show matching and missing skills  
• Generate resume summaries, cover letters, and outreach messages
""")


candidate_name = st.text_input(
    "Your Name",
    placeholder="Enter your full name"
)

keyword = st.text_input(
    "Job Keyword",
    value="data scientist"
)

location = st.text_input(
    "Location",
    value="remote"
)

resume_text = st.text_area(
    "Paste Your Resume",
    height=250
)

bio = st.text_input(
    "Short Bio",
    value="I'm a data professional passionate about public service."
)


# -------------------------------------------------
# Fetch Jobs
# -------------------------------------------------

if st.button("Run Job Hunt Assistant"):

    st.write("🔎 Searching for jobs...")

    jobs = fetch_usajobs(keyword, location)

    if not jobs:

        st.error("No jobs found.")

    else:

        jobs = jobs[:5]

        job_descriptions = []

        for job in jobs:

            details = job["MatchedObjectDescriptor"]["UserArea"]["Details"]

            summary = details.get("JobSummary", "")
            duties = details.get("MajorDuties", "")
            qualifications = details.get("Qualifications", "")

            job_text = f"{summary} {duties} {qualifications}"

            job_descriptions.append(job_text)

        scores = compute_similarity(resume_text, job_descriptions)

        st.session_state.jobs = jobs
        st.session_state.job_texts = job_descriptions
        st.session_state.scores = scores


# -------------------------------------------------
# Show Jobs
# -------------------------------------------------

if "jobs" in st.session_state:

    st.subheader("🎯 Recommended Jobs")

    selected_jobs = []

    for i, job in enumerate(st.session_state.jobs):

        descriptor = job["MatchedObjectDescriptor"]

        title = descriptor["PositionTitle"]
        agency = descriptor["OrganizationName"]

        summary = descriptor["UserArea"]["Details"]["JobSummary"]

        job_text = st.session_state.job_texts[i]

        score = st.session_state.scores[i]

        st.markdown("---")

        st.subheader(f"{title} — {agency}")

        st.metric("Match Score", f"{score*100:.1f}%")

        st.write(summary)


        # -------------------------------------------------
        # Skill Analysis
        # -------------------------------------------------

        matching, missing = skill_gap_analysis(
            resume_text,
            job_text
        )

        if not matching and not missing:

            st.info("⚠ Unable to detect technical skills from this job description.")

        else:

            st.markdown("### ✅ Matching Skills")

            if matching:
                for skill in matching:
                    st.write(f"✔ {skill}")
            else:
                st.write("No matching skills found.")


            st.markdown("### ⚠ Missing Skills")

            if missing:
                for skill in missing:
                    st.write(f"✖ {skill}")
            else:
                st.write("No missing skills detected.")


        if st.checkbox("Apply to this job", key=i):

            selected_jobs.append(job)


# -------------------------------------------------
# Run AI Agents
# -------------------------------------------------

    if st.button("Apply to Selected Jobs"):

        for job in selected_jobs:

            descriptor = job["MatchedObjectDescriptor"]

            title = descriptor["PositionTitle"]

            summary = descriptor["UserArea"]["Details"]["JobSummary"]

            st.markdown("---")

            st.markdown(f"## {title}")

            st.markdown("### Job Description")

            st.write(summary)

            with st.spinner("Running AI agents..."):

                result = run_pipeline(
                    job,
                    resume_text,
                    bio,
                    candidate_name
                )

            st.markdown("### ✨ AI Generated Output")

            st.write(result)
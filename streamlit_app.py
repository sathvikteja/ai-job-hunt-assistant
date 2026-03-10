import streamlit as st

from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline


st.set_page_config(
    page_title="AI Job Hunt Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Job Hunt Assistant")

st.markdown("""
This app uses AI agents to help with your job search.

The system will:

1. Analyze job descriptions
2. Generate a tailored resume summary
3. Generate a cover letter
4. Generate an outreach message
""")


# -----------------------------
# User Inputs
# -----------------------------

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


# -----------------------------
# Fetch jobs
# -----------------------------

if st.button("Run Job Hunt Assistant"):

    st.write("🔎 Searching for jobs...")

    jobs = fetch_usajobs(keyword, location)

    if not jobs:
        st.error("No jobs found for this keyword/location.")
    else:

        st.session_state.jobs = jobs[:5]


# -----------------------------
# Show jobs
# -----------------------------

if "jobs" in st.session_state:

    st.subheader("Select Jobs to Apply")

    selected_jobs = []

    for i, job in enumerate(st.session_state.jobs):

        descriptor = job["MatchedObjectDescriptor"]

        title = descriptor["PositionTitle"]
        agency = descriptor["OrganizationName"]

        if st.checkbox(f"{title} — {agency}", key=i):
            selected_jobs.append(job)

    if st.button("Apply to Selected Jobs"):

        for job in selected_jobs:

            descriptor = job["MatchedObjectDescriptor"]

            title = descriptor["PositionTitle"]
            agency = descriptor["OrganizationName"]

            st.markdown(f"## {title}")
            st.markdown("### Job Description")

            summary = descriptor["UserArea"]["Details"]["JobSummary"]

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
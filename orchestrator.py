from crewai import Crew, Process

from agents.jd_analyst import get_jd_agent, create_jd_task
from agents.resume_cl_agent import get_resume_agent, create_resume_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task

from utils.tracking import log_application, save_cover_letter_file


def extract_between_markers(text, start_marker, end_marker=None):
    """
    Extract text between markers.
    If end_marker is None, extract everything after start_marker.
    """
    try:
        start = text.index(start_marker) + len(start_marker)

        if end_marker:
            end = text.index(end_marker)
            return text[start:end].strip()
        else:
            return text[start:].strip()

    except ValueError:
        return ""


def run_pipeline(job_data, resume_text, user_bio, candidate_name):

    # ------------------------------
    # Extract job info
    # ------------------------------

    # Case 1: simplified object from Streamlit
    if "title" in job_data:
        job_title = job_data.get("title", "Unknown Role")
        agency_name = job_data.get("agency", "Unknown Agency")
        job_summary = job_data.get("summary", "No summary provided")

    # Case 2: raw USAJobs API object
    else:
        descriptor = job_data.get("MatchedObjectDescriptor", {})

        job_title = descriptor.get("PositionTitle", "Unknown Role")
        agency_name = descriptor.get("OrganizationName", "Unknown Agency")

        job_summary = (
            descriptor.get("UserArea", {})
            .get("Details", {})
            .get("JobSummary", "No summary provided")
        )

    # ------------------------------
    # Initialize Agents
    # ------------------------------

    jd_agent = get_jd_agent()
    resume_agent = get_resume_agent()
    messaging_agent = get_messaging_agent()

    # ------------------------------
    # Create Tasks
    # ------------------------------

    jd_task = create_jd_task(jd_agent, job_summary)

    resume_task = create_resume_task(
        resume_agent,
        job_summary,
        resume_text
    )

    messaging_task = create_messaging_task(
        messaging_agent,
        job_summary,
        agency_name,
        user_bio,
        candidate_name
    )

    # ------------------------------
    # Create Crew
    # ------------------------------

    crew = Crew(
        agents=[jd_agent, resume_agent, messaging_agent],
        tasks=[jd_task, resume_task, messaging_task],
        process=Process.sequential,
        verbose=True
    )

    # ------------------------------
    # Run Crew
    # ------------------------------

    result = crew.kickoff()

    # ------------------------------
    # Extract Resume Agent Output
    # ------------------------------

    resume_output = str(resume_task.output)

    print("\n----- RESUME AGENT OUTPUT -----")
    print(resume_output)
    print("--------------------------------\n")

    resume_summary = extract_between_markers(
        resume_output,
        "<<RESUME_SUMMARY>>",
        "<<COVER_LETTER>>"
    )

    cover_letter = extract_between_markers(
        resume_output,
        "<<COVER_LETTER>>"
    )

    if not cover_letter:
        cover_letter = resume_output

    # ------------------------------
    # Log application
    # ------------------------------

    log_application(
        job_title,
        agency_name,
        resume_summary
    )

    # ------------------------------
    # Save cover letter
    # ------------------------------

    save_cover_letter_file(
        job_title,
        agency_name,
        cover_letter
    )

    return str(result)
from crewai import Agent, Task


def get_resume_agent():

    agent = Agent(
        role="Resume and Cover Letter Writer",
        goal="Generate a tailored resume summary and professional cover letter.",
        backstory=(
            "You are an expert career coach and resume writer who specializes in "
            "tailoring resumes and writing strong cover letters for job applications."
        ),
        llm="ollama/llama3",
        verbose=True
    )

    return agent


def create_resume_task(agent, job_summary, resume_text):

    prompt = f"""
You are helping a candidate apply for a job.

JOB SUMMARY:
{job_summary}

CANDIDATE RESUME:
{resume_text}

Your tasks:

1. Tailor the candidate's resume summary to align with the job role.
2. Generate a professional cover letter.

Output format:

<<RESUME_SUMMARY>>
Write a tailored resume summary here.

<<COVER_LETTER>>
Write a professional cover letter here.
"""

    task = Task(
        description=prompt,
        agent=agent,
        expected_output="A tailored resume summary and a professional cover letter."
    )

    return task
from crewai import Agent, Task


def get_messaging_agent():
    """
    Creates the messaging agent responsible for writing outreach messages
    to recruiters or hiring managers.
    """

    agent = Agent(
        role="Job Outreach Specialist",
        goal="Write short, professional outreach messages to hiring managers or recruiters.",
        backstory=(
            "You are an expert networking assistant who helps job seekers craft "
            "professional outreach messages to recruiters and hiring managers. "
            "Your messages are concise, polite, and highlight the candidate's interest "
            "in the role and organization."
        ),
        llm="ollama/llama3",
        verbose=True
    )

    return agent


def create_messaging_task(agent, job_summary, agency_name, user_bio, candidate_name):
    """
    Creates a task for generating a recruiter outreach message.
    """

    prompt = f"""
You are helping a job seeker write a short outreach message.

CANDIDATE NAME:
{candidate_name}

JOB SUMMARY:
{job_summary}

AGENCY / ORGANIZATION:
{agency_name}

CANDIDATE BIO:
{user_bio}

Write a short professional outreach message expressing interest in the role.

Requirements:
- Maximum 120 words
- Professional tone
- Mention interest in the role
- Briefly highlight the candidate's background
- Always use the candidate name "{candidate_name}" instead of placeholders
- Do not invent experience not present in the candidate background
"""

    task = Task(
        description=prompt,
        agent=agent,
        expected_output="A concise professional outreach message under 150 words."
    )

    return task
from crewai import Agent, Task


def get_jd_agent():

    agent = Agent(
        role="Job Description Analyst",
        goal="Analyze job descriptions and extract key information.",
        backstory=(
            "You are an expert HR analyst who reads job descriptions "
            "and extracts structured information about roles, responsibilities, "
            "required skills, and qualifications."
        ),
        llm="ollama/llama3",
        verbose=True
    )

    return agent


def create_jd_task(agent, job_description):

    prompt = f"""
Analyze the following job description and extract key information.

Job Description:
{job_description}

Identify:

- Job summary
- Key responsibilities
- Required skills
- Qualifications
"""

    task = Task(
        description=prompt,
        agent=agent,
        expected_output="A structured analysis of the job description."
    )

    return task
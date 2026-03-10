from sklearn.metrics.pairwise import cosine_similarity
from utils.embeddings import get_embedding, get_embeddings


def compute_similarity(resume_text, job_descriptions):
    """
    Compute cosine similarity between resume and job descriptions.
    """

    resume_embedding = get_embedding(resume_text)

    job_embeddings = get_embeddings(job_descriptions)

    scores = cosine_similarity(
        [resume_embedding],
        job_embeddings
    )[0]

    return scores


def skill_overlap(resume_text, job_description):
    """
    Calculate simple skill overlap between resume and job description.
    """

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    overlap = resume_words.intersection(job_words)

    if len(job_words) == 0:
        return 0

    return len(overlap) / len(job_words)


def compute_final_score(similarity, skill_score):
    """
    Combine similarity + skill match.
    """

    final_score = (
        0.7 * similarity +
        0.3 * skill_score
    )

    return final_score


def rank_jobs(resume_text, job_descriptions):
    """
    Rank jobs based on final score.
    """

    similarities = compute_similarity(resume_text, job_descriptions)

    results = []

    for i, job in enumerate(job_descriptions):

        skill_score = skill_overlap(resume_text, job)

        final_score = compute_final_score(
            similarities[i],
            skill_score
        )

        results.append(final_score)

    return results
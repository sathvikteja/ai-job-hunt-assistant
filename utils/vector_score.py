import faiss
import numpy as np
from utils.embeddings import get_embeddings, get_embedding


class JobVectorStore:

    def __init__(self, jobs):

        """
        Initialize FAISS index with job descriptions
        """

        self.jobs = jobs

        job_descriptions = [
            job["MatchedObjectDescriptor"]["UserArea"]["Details"]["JobSummary"]
            for job in jobs
        ]

        embeddings = get_embeddings(job_descriptions)

        self.embeddings = np.array(embeddings).astype("float32")

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(self.embeddings)

    def search(self, resume_text, k=5):

        """
        Retrieve top K similar jobs
        """

        query_embedding = get_embedding(resume_text)

        query_embedding = np.array([query_embedding]).astype("float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []

        for idx in indices[0]:

            results.append(self.jobs[idx])

        return results
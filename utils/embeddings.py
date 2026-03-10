from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str):
    """
    Convert text into embedding vector.
    """

    if not text:
        text = ""

    embedding = model.encode(text)

    return embedding


def get_embeddings(text_list):
    """
    Convert list of texts to embeddings.
    """

    if not text_list:
        return []

    embeddings = model.encode(text_list)

    return embeddings
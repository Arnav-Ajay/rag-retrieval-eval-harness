# retriever.py → embeddings + top-K
import numpy as np

def get_embedding(chunk: str) -> np.ndarray:
    """
    Diagnostic embedding used only to illustrate retrieval behavior.
    This is intentionally simplistic and NOT a semantic embedding.
    Replace with a real embedding model for practical use.
    """
    embedding_size = 128
    embedding = np.zeros(embedding_size)
    for i, char in enumerate(chunk):
        if i < embedding_size:
            embedding[i] = ord(char)
    return embedding

def create_vector_store(chunks):
    """
    Build an in-memory vector store from chunked documents.

    Each entry is a tuple:
        (chunk_id, doc_id, chunk_text, embedding)

    This function preserves document provenance explicitly to support
    retrieval inspection and evaluation.
    """

    vector_store = []
    for chunk_id, chunk_info in chunks.items():
        chunk_text = chunk_info["text"]
        doc_id = chunk_info["doc_id"]
        embedding = get_embedding(chunk_text)
        vector_store.append((chunk_id, doc_id, chunk_text, embedding))
    return vector_store

def cosine_similarity(vec1, vec2):
    """
    Compute cosine similarity between two vectors.
    Returns 0.0 if either vector has zero magnitude.
    """
    dot_product = np.dot(vec1, vec2.T)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

def retrieve_similar_documents(vector_store, query, top_k=4):
    """
    Retrieve the top-K most similar chunks for a query.

    This function performs a simple similarity-based ranking over the
    entire vector store and returns the highest-scoring results.

    Note:
    - This is a diagnostic retrieval function, not a production retriever.
    - Ranking behavior is intentionally transparent for evaluation.
    """

    query_embedding = get_embedding(query)
    similarities = []

    for chunk_id, doc_id, chunk_text, embedding in vector_store:
        sim = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk_id, doc_id, chunk_text, sim))

    similarities.sort(key=lambda x: x[3], reverse=True)

    return similarities[:top_k]



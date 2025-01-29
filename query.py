import json
import numpy as np
from db import get_connection
from embedding import generate_embedding
from numpy.linalg import norm


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (norm(vec1) * norm(vec2))


def find_similar_text(query_text):
    """Find similar texts from MySQL database."""
    query_embedding = generate_embedding(query_text)

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all stored embeddings
    cursor.execute("SELECT text, embedding FROM text_embeddings")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    similarities = []
    for stored_text, stored_embedding in results:
        stored_embedding = np.array(
            json.loads(stored_embedding)
        )  # Convert JSON to numpy array
        similarity = cosine_similarity(query_embedding, stored_embedding)
        similarities.append((stored_text, similarity))

    # Sort by highest similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:5]  # Return top 5 matches


# Example Usage
if __name__ == "__main__":
    query_text = "Find similar sentences."
    similar_texts = find_similar_text(query_text)
    print("Top Matches:")
    for text, score in similar_texts:
        print(f"{text} (Similarity: {score:.4f})")

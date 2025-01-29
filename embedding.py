from sentence_transformers import SentenceTransformer

# Load the SBERT model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    """Generate embeddings for a given text."""
    return model.encode(text).tolist()  # Convert to list for JSON storage

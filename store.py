import json
from db import get_connection
from embedding import generate_embedding


def store_text_embedding(text):
    """Insert text and its embedding into MySQL if it doesn't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if text already exists
    cursor.execute("SELECT COUNT(*) FROM text_embeddings WHERE text = %s", (text,))
    if cursor.fetchone()[0] > 0:
        print(f"Text already exists: {text}")
        cursor.close()
        conn.close()
        return

    # Generate embedding and store if text is unique
    embedding = generate_embedding(text)
    
    # Insert into MySQL
    cursor.execute(
        "INSERT INTO text_embeddings (text, embedding) VALUES (%s, %s)",
        (text, json.dumps(embedding)),  # Store embedding as JSON
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Stored: {text}")


# Example Usage
if __name__ == "__main__":
    sample_texts = [
        "This is a sample sentence.",
        "Another example for embedding storage.",
    ]
    for text in sample_texts:
        store_text_embedding(text)

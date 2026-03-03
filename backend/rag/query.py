from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv
load_dotenv()
# Same settings as ingest.py
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "cbam_regulations"


def query_rag(question: str) -> str:

    # Step 1: Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Step 2: Use same embeddings as ingest
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Step 3: Convert question into a vector
    question_vector = embeddings.embed_query(question)

    # Step 4: Search Qdrant points using vector similarity
    # Returns top 4 most relevant points (chunks)
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        limit=4,                         # top 4 relevant chunks
    )
    results = response.points

    # Step 5: Extract text from each point's payload
    context_parts = []
    for point in results:
        payload = point.payload or {}
        text = payload.get("text", "")
        source = payload.get("source", "")
        context_parts.append(f"[Source: {source}]\n{text}")

    # Step 6: Join all chunks into one context string
    context = "\n\n".join(context_parts)

    return context


# Test it directly
# python -m rag.query
if __name__ == "__main__":
    test_question = "Is hot rolled steel covered under CBAM Annex I?"
    result = query_rag(test_question)
    print(result)

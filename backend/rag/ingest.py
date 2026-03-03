import os
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Settings
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "cbam_regulations"

# PDFs to load
PDF_FILES = [
    "data/CBAM_Regulation.pdf",
    "data/CN-code.pdf",
    "data/COMMISSION_IMPLEMENTING_REGULATION_2026.pdf",
    "data/Default_emission_values_transitional_period.pdf",
]


def ingest_documents():

    # Step 1: Load all PDFs
    all_documents = []

    for pdf_path in PDF_FILES:
        print(f"Loading {pdf_path}...")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        all_documents.extend(pages)

    print(f"Total pages loaded: {len(all_documents)}")

    # Step 2: Split into small chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(all_documents)
    print(f"Total chunks created: {len(chunks)}")

    # Step 3: Connect to Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # Step 4: Create collection in Qdrant (only first time)
    existing = [c.name for c in client.get_collections().collections]

    if COLLECTION_NAME not in existing:
        print("Creating Qdrant collection...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
    else:
        print("Collection already exists, skipping creation.")

    # Step 5: Create embeddings
    print("Creating embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Step 6: Convert each chunk into a Qdrant point
    # point = vector + payload (text + metadata)
    # This is faster than LangChain wrapper because we control it directly
    points = []

    for i, chunk in enumerate(chunks):

        # Create vector from chunk text
        vector = embeddings.embed_query(chunk.page_content)

        # Build the point
        point = PointStruct(
            id=str(uuid.uuid4()),        # unique id for each chunk
            vector=vector,               # the embedding vector for fast search
            payload={
                "text": chunk.page_content,                   # actual text
                "source": chunk.metadata.get("source", ""),  # which PDF file
                "page": chunk.metadata.get("page", 0)        # page number
            }
        )
        points.append(point)

        if i % 50 == 0:
            print(f"Processed {i}/{len(chunks)} chunks...")

    # Step 7: Upload all points to Qdrant at once
    print("Uploading points to Qdrant in batches...")
    batch_size = 50

    for i in range(0, len(points), batch_size):
        batch = points[i: i + batch_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )
        print(f"Uploaded batch {i // batch_size + 1} / {len(points) // batch_size + 1}")


    print(f"Done! {len(points)} points stored in Qdrant.")


# Run this once before starting the pipeline
# python -m rag.ingest
if __name__ == "__main__":
    ingest_documents()
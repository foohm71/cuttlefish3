import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import openai

load_dotenv()

QDRANT_URL = os.environ.get('QDRANT_URL')
QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')
QDRANT_COLLECTION = os.environ.get('QDRANT_COLLECTION', 'cuttlefish3')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_EMBED_MODEL = os.environ.get('OPENAI_EMBED_MODEL', 'text-embedding-3-small')

openai.api_key = OPENAI_API_KEY

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

print(f"Connecting to Qdrant at {QDRANT_URL} ...")

# List all collections to verify connectivity
try:
    collections = client.get_collections()
    print("Qdrant is reachable. Collections available:")
    for collection in collections.collections:
        print(f"- {collection.name}")
    print("Sanity test completed successfully.")
except Exception as e:
    print(f"Failed to connect or query Qdrant: {e}")

# Query for similar data to a test sentence
query_text = "The quick brown fox jumps over the lazy dog"
print(f"\nQuerying for similar items to: '{query_text}'")
try:
    response = openai.embeddings.create(
        input=query_text,
        model=OPENAI_EMBED_MODEL
    )
    query_vector = response.data[0].embedding
    results = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_vector,
        limit=5
    )
    print(f"Top 5 similar items in '{QDRANT_COLLECTION}':")
    for hit in results:
        print(f"ID: {hit.id}, Score: {hit.score:.4f}, Payload: {hit.payload}")
except Exception as e:
    print(f"Failed to perform similarity search: {e}") 

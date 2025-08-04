import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.environ.get('QDRANT_URL')
QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

collections = client.get_collections().collections
print("Collections to be deleted:")
for collection in collections:
    print(f"- {collection.name}")

confirm = input("Are you sure you want to delete ALL collections? Type 'yes' to confirm: ")
if confirm.lower() == 'yes':
    for collection in collections:
        print(f"Deleting collection: {collection.name}")
        client.delete_collection(collection_name=collection.name)
    print("All collections deleted.")
else:
    print("Aborted. No collections were deleted.") 
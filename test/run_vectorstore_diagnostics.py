#!/usr/bin/env python3
"""
Run vectorstore diagnostics on existing QDrant instance
"""

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

# Import the diagnostics
from vectorstore_diagnostics import diagnose_content_issue

def connect_to_existing_vectorstore():
    """Connect to the existing QDrant vectorstore."""
    print("🔧 Connecting to existing QDrant vectorstore...")
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from .env
    qdrant_url = os.environ.get('QDRANT_URL')
    qdrant_api_key = os.environ.get('QDRANT_API_KEY')
    collection_name = os.environ.get('QDRANT_COLLECTION', 'cuttlefish3')
    
    print(f"Connecting to Qdrant at: {qdrant_url}")
    print(f"Collection name: {collection_name}")
    
    try:
        # Create Qdrant client
        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        
        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        
        if collection_name not in collection_names:
            print(f"❌ Collection '{collection_name}' not found!")
            print(f"Available collections: {collection_names}")
            return None
        
        print(f"✅ Found collection '{collection_name}'")
        
        # Get collection info
        collection_info = client.get_collection(collection_name)
        print(f"Collection info: {collection_info}")
        
        # Set up embeddings
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        
        # Create LangChain vectorstore wrapper
        vectorstore = Qdrant(
            client=client,
            collection_name=collection_name,
            embeddings=embeddings
        )
        
        print("✅ Successfully connected to existing vectorstore")
        return vectorstore
        
    except Exception as e:
        print(f"❌ Error connecting to vectorstore: {e}")
        return None

def main():
    """Main function to run diagnostics on existing vectorstore."""
    print("🚀 CUTTLEFISH3 EXISTING VECTORSTORE DIAGNOSTICS")
    print("=" * 80)
    
    # Connect to existing vectorstore
    vectorstore = connect_to_existing_vectorstore()
    
    if vectorstore:
        # Run diagnostics
        diagnose_content_issue(vectorstore)
    else:
        print("❌ Could not connect to existing vectorstore")
        print("Please check your .env configuration and Qdrant connection")

if __name__ == "__main__":
    main() 
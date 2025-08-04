#!/usr/bin/env python3
"""
This script processes JIRA CSV data and uploads them to Qdrant with embeddings.
Modified to store content in LangChain-compatible format.
"""

import pandas as pd
from qdrant_client import QdrantClient
import openai
import argparse
import os
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

QDRANT_URL = os.environ.get('QDRANT_URL')
QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')
COLLECTION_NAME = os.environ.get('QDRANT_COLLECTION', 'cuttlefish3')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_EMBED_MODEL = os.environ.get('OPENAI_EMBED_MODEL', 'text-embedding-3-small')
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', 128))
MAX_CHARS = 16000  # or lower if you want extra safety

openai.api_key = OPENAI_API_KEY

# --- EMBEDDING FUNCTION ---
def get_embedding(text, model=OPENAI_EMBED_MODEL):
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

def safe_text(text):
    return text[:MAX_CHARS]

# --- MAIN SCRIPT ---
def main(csv_path, start_line=0):
    print(f"Connecting to Qdrant at {QDRANT_URL} ...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    print(f"Ensuring collection '{COLLECTION_NAME}' exists ...")
    
    # Get embedding dimension from OpenAI model metadata (first call)
    print(f"Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path, low_memory=False)
    print(f"Loaded {len(df)} rows.")
    df['title'] = df['title'].fillna("")
    df['description'] = df['description'].fillna("")
    
    # Get embedding dimension
    sample_text = df.iloc[0]['title'] + ' ' + df.iloc[0]['description']
    emb_dim = len(get_embedding(sample_text))
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"size": emb_dim, "distance": "Cosine"}
    )
    
    points = []
    for idx, row in tqdm(df.iloc[start_line:].iterrows(), total=len(df)-start_line):
        # Create the content field that LangChain expects
        title = row['title'].strip()
        description = row['description'].strip()
        
        # Format content as "Title: X\n\nDescription: Y" for better RAG performance
        if title and description:
            content = f"Title: {title}\n\nDescription: {description}"
        elif title:
            content = f"Title: {title}"
        elif description:
            content = f"Description: {description}"
        else:
            content = "No content available"
        
        # Limit content length for embedding
        content = safe_text(content)
        
        try:
            vector = get_embedding(content)
        except Exception as e:
            print(f"Skipping row {row.get('id', idx+start_line)} due to embedding error: {e}")
            continue
        
        # Create payload with content field and metadata
        payload = row.drop(['title', 'description']).to_dict()
        payload['content'] = content  # Add the formatted content for LangChain
        payload['title'] = title      # Keep original title for metadata
        payload['description'] = description  # Keep original description for metadata
        
        points.append({
            "id": int(row['id']) if not pd.isnull(row['id']) else idx+start_line,
            "vector": vector,
            "payload": payload
        })
        
        if len(points) >= BATCH_SIZE:
            try:
                client.upsert(collection_name=COLLECTION_NAME, points=points)
            except Exception as e:
                print(f"Upsert failed at batch starting with row {idx+start_line}: {e}")
            points = []
    
    if points:
        try:
            client.upsert(collection_name=COLLECTION_NAME, points=points)
        except Exception as e:
            print(f"Final upsert failed: {e}")
    print("Upload complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Jira CSV to Qdrant using OpenAI embeddings.")
    parser.add_argument('csv_path', help='Path to JIRA_OPEN_DATA_ALL.csv')
    parser.add_argument('start_line', nargs='?', type=int, default=0, help='Row index to start from (default: 0)')
    args = parser.parse_args()
    main(args.csv_path, args.start_line) 

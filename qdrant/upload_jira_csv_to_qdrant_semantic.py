#!/usr/bin/env python3
"""
Modified version of upload_jira_csv_to_qdrant.py that uses SemanticChunking
to split JIRA documents before uploading to Qdrant vector store.

This script processes JIRA CSV data, applies semantic chunking to create
more coherent document chunks, and uploads them to Qdrant with embeddings.
"""

import pandas as pd
from qdrant_client import QdrantClient
import openai
import argparse
import os
from tqdm import tqdm
from dotenv import load_dotenv
import csv
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
QDRANT_URL = os.environ.get('QDRANT_URL')
QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')
COLLECTION_NAME = os.environ.get('QDRANT_COLLECTION', 'cuttlefish3')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_EMBED_MODEL = os.environ.get('OPENAI_EMBED_MODEL', 'text-embedding-3-small')
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', 128))
MAX_CHARS = 16000  # Maximum characters per chunk for safety

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def safe_text(text):
    """Truncate text to safe length for embedding."""
    return text[:MAX_CHARS] if text else ""

def load_jira_documents(csv_path, max_docs=None):
    """
    Load JIRA documents from CSV file.
    
    Args:
        csv_path (str): Path to JIRA CSV file
        max_docs (int, optional): Maximum number of documents to load
    
    Returns:
        list: List of LangChain Document objects
    """
    print(f"Loading JIRA documents from: {csv_path}")
    
    # Set CSV field size limit for large JIRA descriptions
    csv.field_size_limit(10000000)
    
    documents = []
    
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for i, row in enumerate(reader):
            title = row.get('title', '').strip()
            description = row.get('description', '').strip()
            
            # Skip empty entries
            if not title and not description:
                continue
                
            # Create combined content for better chunking
            if title and description:
                content = f"Title: {title}\n\nDescription: {description}"
            elif title:
                content = f"Title: {title}"
            else:
                content = f"Description: {description}"
            
            # Create document with JIRA metadata
            doc = Document(
                page_content=content,
                metadata={
                    "id": row.get('id', i),
                    "key": row.get('key', ''),
                    "project": row.get('project', ''),
                    "project_name": row.get('project_name', ''),
                    "priority": row.get('priority', ''),
                    "type": row.get('type', ''),
                    "status": row.get('status', ''),
                    "created": row.get('created', ''),
                    "resolved": row.get('resolved', ''),
                    "updated": row.get('updated', ''),
                    "component": row.get('component', ''),
                    "version": row.get('version', ''),
                    "reporter": row.get('reporter', ''),
                    "assignee": row.get('assignee', ''),
                    "title": title,
                    "description_length": len(description),
                    "original_row_index": i
                }
            )
            
            documents.append(doc)
            
            # Limit documents if specified
            if max_docs and len(documents) >= max_docs:
                break
    
    print(f"✅ Loaded {len(documents)} JIRA documents")
    return documents

def create_semantic_chunks(documents, embeddings_model):
    """
    Apply semantic chunking to JIRA documents.
    
    Args:
        documents (list): List of LangChain Document objects
        embeddings_model: OpenAI embeddings model
    
    Returns:
        list: List of semantically chunked documents
    """
    print("Creating semantic chunks...")
    
    # Initialize semantic chunker with same config as notebook
    semantic_chunker = SemanticChunker(
        embeddings_model,
        breakpoint_threshold_type="percentile"
    )
    
    # Apply semantic chunking
    print(f"Processing {len(documents)} documents for semantic chunking...")
    chunked_documents = []
    
    # Process in smaller batches to manage memory and API calls
    batch_size = 50
    for i in tqdm(range(0, len(documents), batch_size), desc="Chunking batches"):
        batch = documents[i:i + batch_size]
        try:
            batch_chunks = semantic_chunker.split_documents(batch)
            
            # Add chunk metadata
            for j, chunk in enumerate(batch_chunks):
                chunk.metadata["chunk_id"] = f"{chunk.metadata.get('id', i)}_{j}"
                chunk.metadata["chunk_index"] = j
                chunk.metadata["total_chunks"] = len(batch_chunks)
                chunk.metadata["chunking_method"] = "semantic"
            
            chunked_documents.extend(batch_chunks)
            
        except Exception as e:
            print(f"⚠️  Error chunking batch {i//batch_size + 1}: {e}")
            # Fall back to original documents for this batch
            chunked_documents.extend(batch)
    
    print(f"✅ Created {len(chunked_documents)} semantic chunks from {len(documents)} documents")
    print(f"   Average chunks per document: {len(chunked_documents)/len(documents):.2f}")
    
    return chunked_documents

def upload_to_qdrant(chunks, client, collection_name, embeddings_model):
    """
    Upload semantic chunks to Qdrant with embeddings.
    
    Args:
        chunks (list): List of chunked documents
        client: Qdrant client
        collection_name (str): Name of the collection
        embeddings_model: OpenAI embeddings model
    """
    print(f"Uploading {len(chunks)} chunks to Qdrant collection '{collection_name}'...")
    
    # Get embedding dimension from first chunk
    sample_text = safe_text(chunks[0].page_content)
    sample_embedding = embeddings_model.embed_query(sample_text)
    emb_dim = len(sample_embedding)
    
    # Recreate collection with proper vector configuration
    print(f"Creating collection with vector dimension: {emb_dim}")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config={"size": emb_dim, "distance": "Cosine"}
    )
    
    # Process chunks in batches
    points = []
    failed_chunks = 0
    
    for i, chunk in enumerate(tqdm(chunks, desc="Processing chunks")):
        try:
            # Generate embedding for chunk content
            text = safe_text(chunk.page_content)
            vector = embeddings_model.embed_query(text)
            
            # Prepare payload with metadata
            payload = chunk.metadata.copy()
            payload['content'] = chunk.page_content
            payload['content_length'] = len(chunk.page_content)
            
            # Convert any non-serializable values to strings
            for key, value in payload.items():
                if pd.isna(value):
                    payload[key] = None
                elif not isinstance(value, (str, int, float, bool, type(None))):
                    payload[key] = str(value)
            
            points.append({
                "id": i,  # Use sequential ID for chunks
                "vector": vector,
                "payload": payload
            })
            
            # Upload batch when reaching batch size
            if len(points) >= BATCH_SIZE:
                try:
                    client.upsert(collection_name=collection_name, points=points)
                    print(f"   Uploaded batch of {len(points)} chunks")
                    points = []
                except Exception as e:
                    print(f"❌ Batch upload failed at chunk {i}: {e}")
                    failed_chunks += len(points)
                    points = []
            
        except Exception as e:
            print(f"⚠️  Error processing chunk {i}: {e}")
            failed_chunks += 1
            continue
    
    # Upload remaining points
    if points:
        try:
            client.upsert(collection_name=collection_name, points=points)
            print(f"   Uploaded final batch of {len(points)} chunks")
        except Exception as e:
            print(f"❌ Final batch upload failed: {e}")
            failed_chunks += len(points)
    
    total_uploaded = len(chunks) - failed_chunks
    print(f"✅ Upload complete: {total_uploaded}/{len(chunks)} chunks uploaded successfully")
    if failed_chunks > 0:
        print(f"⚠️  {failed_chunks} chunks failed to upload")

def main(csv_path, max_docs=None, start_line=0):
    """
    Main function to process JIRA CSV and upload semantic chunks to Qdrant.
    
    Args:
        csv_path (str): Path to JIRA CSV file
        max_docs (int, optional): Maximum number of documents to process
        start_line (int): Row index to start from (for resuming)
    """
    print("🚀 Starting JIRA CSV to Qdrant upload with Semantic Chunking")
    print(f"   CSV Path: {csv_path}")
    print(f"   Max Docs: {max_docs or 'All'}")
    print(f"   Start Line: {start_line}")
    print(f"   Qdrant URL: {QDRANT_URL}")
    print(f"   Collection: {COLLECTION_NAME}")
    print(f"   Embedding Model: {OPENAI_EMBED_MODEL}")
    print(f"   Batch Size: {BATCH_SIZE}")
    
    # Initialize OpenAI embeddings
    print("Initializing OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBED_MODEL)
    
    # Connect to Qdrant
    print(f"Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Load JIRA documents
    documents = load_jira_documents(csv_path, max_docs)
    
    # Apply start_line filtering if specified
    if start_line > 0:
        documents = documents[start_line:]
        print(f"Starting from document {start_line}, processing {len(documents)} documents")
    
    if not documents:
        print("❌ No documents to process")
        return
    
    # Create semantic chunks
    chunks = create_semantic_chunks(documents, embeddings)
    
    if not chunks:
        print("❌ No chunks created")
        return
    
    # Upload to Qdrant
    upload_to_qdrant(chunks, client, COLLECTION_NAME, embeddings)
    
    print("🎉 Process completed successfully!")
    print(f"📊 Summary:")
    print(f"   • Original documents: {len(documents)}")
    print(f"   • Semantic chunks: {len(chunks)}")
    print(f"   • Chunk ratio: {len(chunks)/len(documents):.2f}")
    print(f"   • Collection: {COLLECTION_NAME}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Upload JIRA CSV to Qdrant using Semantic Chunking and OpenAI embeddings.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all documents
  python upload_jira_csv_to_qdrant_semantic.py JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv
  
  # Process first 1000 documents
  python upload_jira_csv_to_qdrant_semantic.py JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv --max-docs 1000
  
  # Resume from document 500
  python upload_jira_csv_to_qdrant_semantic.py JIRA_OPEN_DATA_LARGESET_DATESHIFTED.csv --start-line 500

Environment Variables Required:
  QDRANT_URL - Qdrant server URL
  QDRANT_API_KEY - Qdrant API key  
  OPENAI_API_KEY - OpenAI API key
  QDRANT_COLLECTION - Collection name (default: jira_issues_semantic)
  OPENAI_EMBED_MODEL - Embedding model (default: text-embedding-3-small)
  BATCH_SIZE - Upload batch size (default: 128)
        """
    )
    
    parser.add_argument('csv_path', help='Path to JIRA CSV file')
    parser.add_argument('--max-docs', type=int, help='Maximum number of documents to process')
    parser.add_argument('--start-line', type=int, default=0, 
                       help='Document index to start from (default: 0)')
    
    args = parser.parse_args()
    
    # Validate required environment variables
    required_vars = ['QDRANT_URL', 'QDRANT_API_KEY', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file or environment")
        exit(1)
    
    main(args.csv_path, args.max_docs, args.start_line)

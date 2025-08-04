#!/usr/bin/env python3
"""
Vectorstore Document Structure Diagnostics

This script analyzes the document structure in the Cuttlefish3 vectorstore
to understand why RAG retrievers are getting empty content instead of 
title and description fields.
"""

import os
import sys
from typing import List, Dict, Any
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

def analyze_sample_documents():
    """Analyze the sample documents that should be in the vectorstore."""
    print("📋 Sample Documents Analysis")
    print("=" * 60)
    
    # These are the sample documents from Phase 1 setup
    sample_docs = [
        Document(
            page_content="Title: Memory leak in XML parser\n\nDescription: Application crashes after processing multiple XML files due to memory not being freed properly in Xerces-C++ library.",
            metadata={"key": "HBASE-001", "project": "HBASE", "priority": "Critical", "type": "Bug"}
        ),
        Document(
            page_content="Title: ClassCastException in SAXParserFactory\n\nDescription: Getting ClassCastException when trying to create SAX parser factory in multi-threaded environment.",
            metadata={"key": "FLEX-002", "project": "FLEX", "priority": "Major", "type": "Bug"}
        ),
        Document(
            page_content="Title: Maven archetype generation fails\n\nDescription: Maven archetype:generate command fails with dependency resolution errors in offline mode.",
            metadata={"key": "SPR-003", "project": "SPR", "priority": "Minor", "type": "Bug"}
        ),
        Document(
            page_content="Title: ZooKeeper quota exceeded\n\nDescription: ZooKeeper client throws quota exceeded exception when creating more than 1000 znodes.",
            metadata={"key": "HBASE-004", "project": "HBASE", "priority": "Major", "type": "Bug"}
        ),
        Document(
            page_content="Title: Hibernate lazy loading issue\n\nDescription: LazyInitializationException occurs when accessing lazy-loaded collections outside of session scope.",
            metadata={"key": "JBIDE-005", "project": "JBIDE", "priority": "Critical", "type": "Bug"}
        )
    ]
    
    print(f"Expected documents in vectorstore: {len(sample_docs)}")
    print("\nSample document structure:")
    for i, doc in enumerate(sample_docs[:2]):
        print(f"\nDocument {i+1}:")
        print(f"  page_content length: {len(doc.page_content)}")
        print(f"  page_content preview: {doc.page_content[:100]}...")
        print(f"  metadata: {doc.metadata}")
    
    return sample_docs

def analyze_vectorstore_documents(vectorstore):
    """Analyze actual documents in the vectorstore."""
    print("\n🔍 Vectorstore Analysis")
    print("=" * 60)
    
    try:
        # Get some documents from vectorstore
        docs = vectorstore.similarity_search("test query", k=10)
        
        print(f"Retrieved documents: {len(docs)}")
        
        if not docs:
            print("❌ No documents found in vectorstore!")
            return
        
        # Analyze each document
        empty_content_count = 0
        valid_content_count = 0
        
        for i, doc in enumerate(docs):
            print(f"\nDocument {i+1}:")
            print(f"  Type: {type(doc)}")
            print(f"  Has page_content: {hasattr(doc, 'page_content')}")
            
            if hasattr(doc, 'page_content'):
                content = doc.page_content
                print(f"  page_content type: {type(content)}")
                print(f"  page_content length: {len(content) if content else 0}")
                
                if content and content.strip():
                    print(f"  page_content preview: {content[:100]}...")
                    valid_content_count += 1
                else:
                    print(f"  ❌ page_content is empty or whitespace!")
                    empty_content_count += 1
            else:
                print("  ❌ No page_content attribute!")
                empty_content_count += 1
            
            print(f"  Has metadata: {hasattr(doc, 'metadata')}")
            if hasattr(doc, 'metadata'):
                metadata = doc.metadata
                print(f"  metadata: {metadata}")
                
                # Check if title/description are in metadata instead
                if 'title' in metadata:
                    print(f"  metadata title: {metadata['title']}")
                if 'description' in metadata:
                    print(f"  metadata description: {metadata.get('description', '')[:50]}...")
        
        print(f"\n📊 Summary:")
        print(f"  Valid content documents: {valid_content_count}")
        print(f"  Empty content documents: {empty_content_count}")
        print(f"  Total documents: {len(docs)}")
        
        return docs
        
    except Exception as e:
        print(f"❌ Error analyzing vectorstore: {e}")
        return []

def analyze_document_creation_vs_retrieval():
    """Compare how documents are created vs how they're retrieved."""
    print("\n🔄 Document Creation vs Retrieval Analysis")
    print("=" * 60)
    
    print("Expected document creation process:")
    print("1. CSV data → Document with page_content = 'Title: X\\n\\nDescription: Y'")
    print("2. Document stored in vectorstore with embeddings")
    print("3. Retrieval should return same page_content structure")
    print("\nPossible issues:")
    print("- Document creation didn't populate page_content correctly")
    print("- Vectorstore storage/retrieval corrupted content")
    print("- Content is in metadata instead of page_content")
    print("- Encoding/serialization issues")

def check_vectorstore_setup():
    """Check if vectorstore was set up correctly."""
    print("\n🔧 Vectorstore Setup Check")
    print("=" * 60)
    
    print("Checking environment variables...")
    
    # Check if using remote Qdrant or in-memory
    qdrant_url = os.environ.get('QDRANT_URL')
    qdrant_api_key = os.environ.get('QDRANT_API_KEY')
    
    if qdrant_url and qdrant_api_key:
        print(f"✅ Remote Qdrant configured: {qdrant_url}")
        print("Using remote Qdrant vectorstore")
    else:
        print("⚠️  No remote Qdrant config found")
        print("Should be using in-memory vectorstore with sample data")
    
    print(f"\nOpenAI API Key available: {'OPENAI_API_KEY' in os.environ}")

def diagnose_content_issue(vectorstore):
    """Main diagnostic function to identify content issues."""
    print("🔍 CUTTLEFISH3 VECTORSTORE CONTENT DIAGNOSTICS")
    print("=" * 80)
    
    # Step 1: Analyze expected sample documents
    expected_docs = analyze_sample_documents()
    
    # Step 2: Check vectorstore setup
    check_vectorstore_setup()
    
    # Step 3: Analyze actual vectorstore documents
    actual_docs = analyze_vectorstore_documents(vectorstore)
    
    # Step 4: Compare creation vs retrieval
    analyze_document_creation_vs_retrieval()
    
    # Step 5: Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if not actual_docs:
        print("1. Vectorstore appears empty - check document loading")
        print("2. Verify sample documents were created correctly")
        print("3. Check if using remote vs in-memory vectorstore")
    else:
        empty_count = sum(1 for doc in actual_docs 
                         if not hasattr(doc, 'page_content') or 
                         not doc.page_content or 
                         not doc.page_content.strip())
        
        if empty_count > 0:
            print(f"1. {empty_count} documents have empty page_content")
            print("2. Check document creation process in Phase 1")
            print("3. Verify CSV parsing and Document creation")
            print("4. Consider recreating vectorstore with proper content")
        else:
            print("1. Documents appear to have valid content")
            print("2. Issue might be in retriever implementation")
            print("3. Check filtering functions for over-aggressive filtering")

if __name__ == "__main__":
    print("Run this from the notebook context where vectorstore is available")
    print("Example usage:")
    print("  from vectorstore_diagnostics import diagnose_content_issue")
    print("  diagnose_content_issue(vectorstore)")
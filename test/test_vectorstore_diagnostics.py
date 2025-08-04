#!/usr/bin/env python3
"""
Test script to run vectorstore diagnostics
"""

import os
import sys
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

# Import the diagnostics
from vectorstore_diagnostics import diagnose_content_issue

def setup_test_vectorstore():
    """Set up a test vectorstore with sample documents."""
    print("🔧 Setting up test vectorstore...")
    
    # Sample documents that should be in the vectorstore
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
    
    # Set up embeddings (will use default OpenAI if API key is available)
    try:
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        print("✅ OpenAI embeddings configured")
    except Exception as e:
        print(f"⚠️  OpenAI embeddings not available: {e}")
        print("Using dummy embeddings for testing...")
        # Create a dummy embeddings class for testing
        class DummyEmbeddings:
            def embed_query(self, text):
                return [0.1] * 1536  # Standard embedding size
            def embed_documents(self, texts):
                return [[0.1] * 1536 for _ in texts]
        embeddings = DummyEmbeddings()
    
    # Create vectorstore
    try:
        vectorstore = Qdrant.from_documents(
            sample_docs,
            embeddings,
            location=":memory:",
            collection_name="TestCuttlefish"
        )
        print(f"✅ Created test vectorstore with {len(sample_docs)} documents")
        return vectorstore
    except Exception as e:
        print(f"❌ Error creating vectorstore: {e}")
        return None

def main():
    """Main function to run diagnostics."""
    print("🚀 CUTTLEFISH3 VECTORSTORE DIAGNOSTICS TEST")
    print("=" * 80)
    
    # Set up test vectorstore
    vectorstore = setup_test_vectorstore()
    
    if vectorstore:
        # Run diagnostics
        diagnose_content_issue(vectorstore)
    else:
        print("❌ Could not set up test vectorstore")
        print("Please check your environment and dependencies")

if __name__ == "__main__":
    main() 
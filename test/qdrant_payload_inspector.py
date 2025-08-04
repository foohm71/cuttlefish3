#!/usr/bin/env python3
"""
Qdrant Payload Inspector

This script directly queries the Qdrant database to inspect the actual payload structure
and understand what fields are available for content extraction.
"""

import os
import json
from typing import Dict, Any, List
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchAny
from dotenv import load_dotenv

def load_config():
    """Load Qdrant configuration from environment."""
    load_dotenv()
    
    config = {
        'url': os.environ.get('QDRANT_URL', 'http://localhost:6333'),
        'api_key': os.environ.get('QDRANT_API_KEY'),
        'collection': os.environ.get('QDRANT_COLLECTION', 'jira_issues')
    }
    
    print(f"Qdrant Configuration:")
    print(f"  URL: {config['url']}")
    print(f"  API Key: {'***' + config['api_key'][-4:] if config['api_key'] else 'Not set'}")
    print(f"  Collection: {config['collection']}")
    
    return config

def inspect_collection_info(client: QdrantClient, collection_name: str):
    """Get basic collection information."""
    print(f"\n📊 Collection Information: {collection_name}")
    print("=" * 60)
    
    try:
        collection_info = client.get_collection(collection_name)
        print(f"Status: {collection_info.status}")
        print(f"Points count: {collection_info.points_count:,}")
        print(f"Vector size: {collection_info.config.params.vectors.size}")
        print(f"Distance metric: {collection_info.config.params.vectors.distance}")
        
        return collection_info
    except Exception as e:
        print(f"❌ Error getting collection info: {e}")
        return None

def get_sample_points(client: QdrantClient, collection_name: str, limit: int = 5):
    """Get sample points from the collection."""
    print(f"\n🔍 Sample Points Analysis (limit: {limit})")
    print("=" * 60)
    
    try:
        # Get random sample points
        points = client.scroll(
            collection_name=collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False
        )[0]  # scroll returns (points, next_page_offset)
        
        if not points:
            print("❌ No points found in collection")
            return []
        
        print(f"Retrieved {len(points)} sample points")
        return points
        
    except Exception as e:
        print(f"❌ Error getting sample points: {e}")
        return []

def analyze_point_structure(points: List):
    """Analyze the structure of retrieved points."""
    print(f"\n🔬 Point Structure Analysis")
    print("=" * 60)
    
    if not points:
        print("No points to analyze")
        return
    
    # Analyze each point
    all_payload_keys = set()
    
    for i, point in enumerate(points):
        print(f"\nPoint {i+1}:")
        print(f"  ID: {point.id}")
        print(f"  Has payload: {point.payload is not None}")
        
        if point.payload:
            payload_keys = list(point.payload.keys())
            all_payload_keys.update(payload_keys)
            print(f"  Payload keys: {payload_keys}")
            
            # Show content of each payload field
            for key, value in point.payload.items():
                value_str = str(value)
                if len(value_str) > 100:
                    value_preview = value_str[:100] + "..."
                else:
                    value_preview = value_str
                print(f"    {key}: '{value_preview}'")
        else:
            print("  ❌ No payload data")
    
    # Summary of all payload keys found
    print(f"\n📋 Summary of All Payload Keys Found:")
    print(f"  Total unique keys: {len(all_payload_keys)}")
    for key in sorted(all_payload_keys):
        print(f"    - {key}")
    
    return all_payload_keys

def test_search_functionality(client: QdrantClient, collection_name: str):
    """Test search functionality to see what's returned."""
    print(f"\n🔍 Search Functionality Test")
    print("=" * 60)
    
    try:
        # Create a dummy query vector (we'll use zeros since we just want to see structure)
        # First get the vector size from collection info
        collection_info = client.get_collection(collection_name)
        vector_size = collection_info.config.params.vectors.size
        dummy_vector = [0.0] * vector_size
        
        # Perform search
        search_results = client.search(
            collection_name=collection_name,
            query_vector=dummy_vector,
            limit=3,
            with_payload=True
        )
        
        print(f"Search returned {len(search_results)} results")
        
        for i, hit in enumerate(search_results):
            print(f"\nSearch Result {i+1}:")
            print(f"  ID: {hit.id}")
            print(f"  Score: {hit.score:.4f}")
            print(f"  Payload keys: {list(hit.payload.keys()) if hit.payload else 'None'}")
            
            if hit.payload:
                # Show content-related fields
                content_fields = ['content', 'title', 'description', 'page_content', 'text']
                for field in content_fields:
                    if field in hit.payload:
                        value = hit.payload[field]
                        if isinstance(value, str) and len(value) > 100:
                            preview = value[:100] + "..."
                        else:
                            preview = str(value)
                        print(f"    {field}: '{preview}'")
        
        return search_results
        
    except Exception as e:
        print(f"❌ Error testing search: {e}")
        return []

def compare_with_langchain_format():
    """Show expected LangChain Document format."""
    print(f"\n📚 Expected LangChain Document Format")
    print("=" * 60)
    
    print("LangChain Document structure:")
    print("  - page_content: str  # Main content text")
    print("  - metadata: dict     # Additional data")
    print("")
    print("Expected for JIRA tickets:")
    print("  page_content: 'Title: X\\nDescription: Y'")
    print("  metadata: {'key': 'JIRA-123', 'project': 'PROJECT', ...}")
    print("")
    print("OR alternative payload structure:")
    print("  payload: {")
    print("    'content': 'Title: X\\nDescription: Y',")
    print("    'title': 'X',")
    print("    'description': 'Y',")
    print("    'key': 'JIRA-123',")
    print("    'project': 'PROJECT'")
    print("  }")

def main():
    """Main inspection function."""
    print("🔍 QDRANT PAYLOAD INSPECTOR")
    print("=" * 80)
    
    # Load configuration
    config = load_config()
    
    # Connect to Qdrant
    try:
        client = QdrantClient(
            url=config['url'],
            api_key=config['api_key']
        )
        print("✅ Connected to Qdrant successfully")
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        return
    
    collection_name = config['collection']
    
    # Inspect collection
    collection_info = inspect_collection_info(client, collection_name)
    if not collection_info:
        return
    
    # Get sample points
    sample_points = get_sample_points(client, collection_name, limit=5)
    
    # Analyze structure
    payload_keys = analyze_point_structure(sample_points)
    
    # Test search functionality
    search_results = test_search_functionality(client, collection_name)
    
    # Show expected format
    compare_with_langchain_format()
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if payload_keys:
        content_related = [k for k in payload_keys if k.lower() in ['content', 'title', 'description', 'page_content', 'text']]
        if content_related:
            print(f"✅ Content-related fields found: {content_related}")
            print(f"   → Use these fields for content extraction in RAG agents")
        else:
            print(f"⚠️  No obvious content fields found in: {list(payload_keys)}")
            print(f"   → Check if content is in other fields or needs different extraction")
        
        print(f"\n🔧 Suggested RAG agent update:")
        if 'content' in payload_keys:
            print(f"   content = hit.payload.get('content', '')")
        elif 'title' in payload_keys and 'description' in payload_keys:
            print(f"   title = hit.payload.get('title', '')")
            print(f"   description = hit.payload.get('description', '')")
            print(f"   content = f'Title: {{title}}\\nDescription: {{description}}'")
        else:
            print(f"   # Need to determine correct field mapping")
    else:
        print("❌ No payload data found - check data ingestion process")

if __name__ == "__main__":
    main()
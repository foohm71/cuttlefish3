#!/usr/bin/env python3
"""
Simple Qdrant inspection - to be run from notebook context
"""

def inspect_vectorstore_payload(vectorstore):
    """Inspect what's actually in the vectorstore."""
    print("🔍 VECTORSTORE PAYLOAD INSPECTION")
    print("=" * 60)
    
    # Get sample documents
    try:
        docs = vectorstore.similarity_search("test query", k=5)
        print(f"Retrieved {len(docs)} documents")
        
        if not docs:
            print("❌ No documents found")
            return
        
        all_metadata_keys = set()
        
        for i, doc in enumerate(docs):
            print(f"\n📄 Document {i+1}:")
            print(f"  Type: {type(doc).__name__}")
            
            # Check page_content
            if hasattr(doc, 'page_content'):
                content = doc.page_content
                print(f"  page_content type: {type(content)}")
                print(f"  page_content length: {len(content) if content else 0}")
                if content and content.strip():
                    print(f"  page_content preview: '{content[:100]}...'")
                else:
                    print(f"  page_content: EMPTY or WHITESPACE")
            
            # Check metadata
            if hasattr(doc, 'metadata'):
                metadata = doc.metadata
                print(f"  metadata type: {type(metadata)}")
                print(f"  metadata keys: {list(metadata.keys()) if metadata else 'None'}")
                
                if metadata:
                    all_metadata_keys.update(metadata.keys())
                    
                    # Show all fields
                    for key, value in metadata.items():
                        value_str = str(value) if value is not None else 'None'
                        if len(value_str) > 100:
                            value_preview = value_str[:100] + "..."
                        else:
                            value_preview = value_str
                        print(f"    {key}: '{value_preview}'")
        
        # Summary
        print(f"\n📊 SUMMARY:")
        print(f"  Total documents analyzed: {len(docs)}")
        print(f"  All metadata keys found: {sorted(all_metadata_keys)}")
        
        # Check for content fields
        content_fields = ['content', 'title', 'description', 'page_content', 'text']
        found_content_fields = [f for f in content_fields if f in all_metadata_keys]
        
        print(f"  Content-related fields: {found_content_fields}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if found_content_fields:
            print(f"  ✅ Use these fields for content extraction: {found_content_fields}")
            if 'content' in found_content_fields:
                print(f"     → content = doc.metadata.get('content', '')")
            elif 'title' in found_content_fields and 'description' in found_content_fields:
                print(f"     → title = doc.metadata.get('title', '')")
                print(f"     → description = doc.metadata.get('description', '')")
                print(f"     → content = f'Title: {{title}}\\\\nDescription: {{description}}'")
        else:
            print(f"  ⚠️  No obvious content fields found")
            print(f"     → Check if data needs to be re-ingested with proper content field")
        
        return docs
        
    except Exception as e:
        print(f"❌ Error inspecting vectorstore: {e}")
        import traceback
        traceback.print_exc()
        return []

def inspect_direct_qdrant_client(qdrant_url, qdrant_api_key, collection_name):
    """If we have direct Qdrant access, inspect that too."""
    print(f"\n🔗 DIRECT QDRANT CLIENT INSPECTION")
    print("=" * 60)
    
    if not qdrant_url or not qdrant_api_key:
        print("❌ No direct Qdrant credentials available")
        return
    
    try:
        # This would require qdrant_client to be installed
        print(f"Would query: {qdrant_url}/{collection_name}")
        print("Need qdrant_client package for direct inspection")
        
    except Exception as e:
        print(f"❌ Error with direct Qdrant access: {e}")

# Usage instructions
print("""
📋 USAGE INSTRUCTIONS:

1. From your notebook, import this module:
   from inspect_qdrant_simple import inspect_vectorstore_payload

2. Run the inspection:
   inspect_vectorstore_payload(vectorstore)

3. This will show exactly what fields are available in your documents
   and recommend how to extract content for the RAG agents.
""")
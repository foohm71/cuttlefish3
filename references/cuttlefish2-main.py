from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any
import openai
import os
from qdrant_client import QdrantClient
from dotenv import load_dotenv
from mangum import Mangum

load_dotenv()

QDRANT_URL = os.environ.get('QDRANT_URL')
QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY')
QDRANT_COLLECTION = os.environ.get('QDRANT_COLLECTION', 'jira_issues')
OPENAI_EMBED_MODEL = os.environ.get('OPENAI_EMBED_MODEL', 'text-embedding-3-small')
OPENAI_RAG_MODEL = os.environ.get('OPENAI_RAG_MODEL', 'gpt-3.5-turbo')

app = FastAPI()

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

class QueryRequest(BaseModel):
    query: str
    openai_api_key: str

class SimilarResult(BaseModel):
    id: Any
    score: float
    payload: dict

class SimilarResponse(BaseModel):
    results: List[SimilarResult]

class RagResponse(BaseModel):
    answer: str
    context: List[SimilarResult]

def get_embedding(query: str, openai_api_key: str) -> list:
    openai.api_key = openai_api_key
    response = openai.embeddings.create(
        input=query,
        model=OPENAI_EMBED_MODEL
    )
    return response.data[0].embedding

@app.post("/similar", response_model=SimilarResponse)
def similar(request: QueryRequest):
    try:
        embedding = get_embedding(request.query, request.openai_api_key)
        results = client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=embedding,
            limit=5
        )
        response = SimilarResponse(
            results=[
                SimilarResult(id=hit.id, score=hit.score, payload=hit.payload)
                for hit in results
            ]
        )
        return response
    except Exception as e:
        print(f"[ERROR] /similar endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rag", response_model=RagResponse)
def rag(request: QueryRequest):
    try:
        embedding = get_embedding(request.query, request.openai_api_key)
        results = client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=embedding,
            limit=5
        )
        context_texts = []
        for hit in results:
            # Use title + description for context
            title = hit.payload.get('title', '') if hit.payload else ''
            description = hit.payload.get('description', '') if hit.payload else ''
            context_texts.append(f"Title: {title}\nDescription: {description}")
        context_str = "\n---\n".join(context_texts)
        prompt = (
            f"You are a helpful assistant. Use the following context to answer the user's question.\n"
            f"Context:\n{context_str}\n\nQuestion: {request.query}\nAnswer:"
        )
        openai.api_key = request.openai_api_key
        completion = openai.chat.completions.create(
            model=OPENAI_RAG_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.2
        )
        answer = completion.choices[0].message.content.strip() if completion.choices and completion.choices[0].message and completion.choices[0].message.content else "No answer generated."
        response = RagResponse(
            answer=answer,
            context=[
                SimilarResult(id=hit.id, score=hit.score, payload=hit.payload)
                for hit in results
            ]
        )
        return response
    except Exception as e:
        print(f"[ERROR] /rag endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app) 
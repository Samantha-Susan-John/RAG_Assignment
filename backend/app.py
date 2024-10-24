from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import faiss
import json
from backend.models.language_model import LanguageModel 
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('data/chunks.json', 'r') as f:
    chunks = json.load(f)

index = faiss.read_index('data/faiss_index.bin')
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
language_model = LanguageModel() 

@app.post('/query')
async def query_ncert(request: Request):
    data = await request.json()
    query = data['question']

    query_embedding = embedding_model.encode([query])
    faiss.normalize_L2(query_embedding)
    
    D, I = index.search(query_embedding, k=2)
    
    response_chunks = [chunks[i] for i in I[0]]

    raw_response = "\n\n".join(response_chunks)
    cleaned_response = re.sub(r'\n', '', raw_response)
    
    formatted_response = cleaned_response.replace("\n", "\n")

    response = language_model(query, formatted_response)
    return {"response": response, "formatted_response": formatted_response}

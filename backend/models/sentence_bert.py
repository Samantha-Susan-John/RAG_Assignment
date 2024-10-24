import json
from sentence_transformers import SentenceTransformer
from backend.utils.text_processing import chunk_text
import torch

with open('data/ncert_combined_text.txt', 'r') as f:
    ncert_text = f.read()

chunks = chunk_text(ncert_text)

def generate_embeddings(chunks):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(chunks, convert_to_tensor=True)
    return embeddings

embeddings = generate_embeddings(chunks)

torch.save(embeddings, 'data/embeddings.pt')

with open('data/chunks.json', 'w') as f:
    json.dump(chunks, f)
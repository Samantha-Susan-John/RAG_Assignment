import faiss
import numpy as np
import torch

# Load the saved embeddings
embeddings = torch.load('data/embeddings.pt')
print(embeddings.shape)

def create_faiss_index(embeddings):
    """Create a FAISS index for fast similarity search."""
    embeddings = embeddings.cpu()  # Move tensor to CPU
    index = faiss.IndexFlatL2(embeddings.shape[1])
    faiss.normalize_L2(embeddings.numpy())  # Normalize for cosine similarity
    index.add(embeddings.numpy())
    return index

index = create_faiss_index(embeddings)
faiss.write_index(index, 'data/faiss_index.bin')
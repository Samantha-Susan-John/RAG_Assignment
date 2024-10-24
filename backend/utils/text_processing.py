from transformers import AutoTokenizer
from typing import List

def chunk_text(text: str, max_tokens: int = 1000) -> List[str]:

    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
    
    # Split text into sentences
    sentences = text.split('. ')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip() + '. '
        
        sentence_tokens = tokenizer.encode(sentence)
        sentence_length = len(sentence_tokens)
        
        if current_length + sentence_length > max_tokens and current_chunk:
            chunks.append(''.join(current_chunk).strip())
            current_chunk = []
            current_length = 0
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    if current_chunk:
        chunks.append(''.join(current_chunk).strip())
    
    return chunks
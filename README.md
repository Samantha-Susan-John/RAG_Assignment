# Building a RAG System




##### Dataset Used: 
NCERT PDF text : Used NCERT text books for all Science subjects (Physics, Chemistry, Biology) from grade 10 to 12. 

##### Vector Database Used:
**FAISS** (Facebook AI Similarity Search) for fast similarity search to retrieve most relevant chunks based on cosine similarity.
Retrieved top 2 most similar chunks stored in the FAISS Index.

##### Models:
- Embeddings generated by SentenceTransformer `sentence-transformers/all-MiniLM-L6-v2` 
- **LLM** : Bloom 560 Million parameters `bigscience/bloom-560m` and `bigscience/bloom-1b1`

##### API Endpoint:
FastAPI endpoint at `'/query'`.

#### RAG System Architecture:
<img width="1253" alt="image" src="https://github.com/user-attachments/assets/0975fee3-2098-4f0d-a543-b6a015d56aaf">

#### Components Breakdown:

1. Data Retrieval Module:

- Text extraction from PDFs using PyMuPDF (fitz)
- Text chunking with transformers tokenizer (max 1000 tokens per chunk)
- Vector embeddings generation using SentenceTransformer
- FAISS index for fast similarity search
- Retrieval Process
	`query_embedding = embedding_model.encode([query])

	`faiss.normalize_L2(query_embedding)`

	`D, I = index.search(query_embedding, k=2)`

2. Language Model Integration:

- Uses BLOOM 560M and BLOOM 1B model for response generation
- "Query before the query", where context provided along with user query in the prompt template given to the LLM

3. API Endpoint:

- FastAPI endpoint at '/query'
- Handles POST requests with JSON payload

4. React Frontend:

- Provides a simple query interface to interact with the LLM
- Retrieved Context button provided to display the top retrieved chunks (provided as context) optionally

#### RAG System Architecture:
---
#### Results:

Used **Bloom 560M** (Open Source) LLM due to its lower computational requirements. However, the model was not able to provide coherent or correct responses. Due to these model hallucinations, the output was at times fabricated and the context ignored.

Provided Prompt template:
`prompt_template = """`

`Below is some relevant context information, followed by a question.`
`You are to help users by answering their questions based on the context provided.`
`Please adhere strictly to the context and provide a detailed answer based only on the context.`
`Keep your response concise and to the point.`
`*DON'T* include additional questions, links or code in the answer.`

`Context: {context}`

`Question: {query}`

`Answer:`

`"""`

Hyperparamters used:

	max_new_tokens=max_length,
	
	num_return_sequences=1,
	
	temperature=0.1,
	
	top_p=0.5,
	
	repetition_penalty=1.2,
	
	do_sample=True,
	
	pad_token_id=self.tokenizer.eos_token_id

<img width="529" alt="image" src="https://github.com/user-attachments/assets/b58c58cf-5ca6-45e9-9b16-7e2c2c6b5927">



Retrieved Context button provided to display the retrieved chunks from the dataset:

<img width="655" alt="image" src="https://github.com/user-attachments/assets/32434096-0dc9-4a18-8df1-4e9c42cfc034">




---
Used **Bloom 1B** due to the poor performance of the Bloom 560M LLM for a more coherent response. (Constrained to using smaller models due to the hardware limitations of my personal computer.) Hyperparameters and prompt same as before.
Bloom 1B provided a much better response.

<img width="630" alt="image" src="https://github.com/user-attachments/assets/c79e8ac8-7ccb-4615-8f69-37aed7f71cb8">

LLMs such as Perplexity AI and Github Copilot were used to identify and solve errors as well as provide useful changes to the code.
All necessary dependencies are listed in the `backend/requirements.txt` file.

To run the backend: Run `uvicorn backend.app:app --reload` in the terminal.

For the frontend: `npm start`

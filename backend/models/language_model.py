from transformers import BloomForCausalLM, BloomTokenizerFast, pipeline
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch
from typing import List

class LanguageModel:
    def __init__(self, model_name: str = "bigscience/bloom-1b1", device: str = "cpu"):
        self.device = "cuda" if torch.cuda.is_available() and device == "cuda" else "cpu"
        
        self.tokenizer = BloomTokenizerFast.from_pretrained(model_name)
        self.max_length = self.tokenizer.model_max_length
        
        self.model = BloomForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,  
            low_cpu_mem_usage=True  
        )
        
        self.model.to(self.device)

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1  
        )

    def _prepare_prompt(self, context: str, query: str) -> str:        
        prompt_template = """
        Below is some relevant context information, followed by a question.
        You are to help users by answering their questions based on the context provided.
        Please adhere strictly to the context and provide a detailed answer based only on the context.
        Keep your response concise and to the point.
        *DON'T* include additional questions, links or code in the answer.

        Context:
        {context}

        Question: {query}

        Answer:
        """

        return prompt_template.format(context=context.strip(), query=query.strip())


    def generate_response(self, query: str, context_chunks: List[str], max_length: int = 1000) -> str:        

        # print(type(context_chunks))

        # context = " ".join(context_chunks)
        context = context_chunks
        try:
            prompt = self._prepare_prompt(context, query)
            print(prompt)
            
            response = self.generator(
                prompt,
                max_new_tokens=max_length,
                num_return_sequences=1,
                temperature=0.1,    
                top_p=0.5,
                repetition_penalty=1.2,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )[0]['generated_text']
            
            answer_start = response.find("Answer:")
            if answer_start != -1:
                response = response[answer_start + len("Answer:"):].strip()
            
            return response

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def __call__(self, query: str, context_chunks: List[str], max_length: int = 1000) -> str:
        return self.generate_response(query, context_chunks, max_length)
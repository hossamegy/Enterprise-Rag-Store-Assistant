import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.core.ports.local_llm import LocalLLM
from src.core.prompts_templetes.rag_template import build_prompt


class LocalLLmImpl(LocalLLM):
    """
    Concrete implementation of the LocalLLM port using a locally-stored
    Qwen2.5-Instruct model loaded via HuggingFace Transformers.
    """

    def __init__(self, model_id: str, device: str, llm_max_token: int):
        self.model_id = model_id
        self.device = device
        self.llm_max_token = llm_max_token
        self.tokenizer, self.model = self.load()

    def load(self) -> tuple:
        print("Loading LLM tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        print("Loading LLM model...")
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
        ).to(self.device)

        model.eval()
        return tokenizer, model

    def rag_answer(self, question_intent: str, processed_question: str, retrieved_context: str) -> str:
        messages = build_prompt(question_intent, processed_question, retrieved_context)
       
        print("messages",messages)
        return self.generate(messages)

    def generate(self, messages: list[dict]) -> str:
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.llm_max_token,
                do_sample=False,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        new_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True)

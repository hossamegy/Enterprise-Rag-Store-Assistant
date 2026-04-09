from google import genai
from src.core.ports.local_llm import LocalLLM
from src.core.prompts_templetes.rag_template import build_prompt

class GeminiLLmImpl(LocalLLM):

    def __init__(self, model_id, api_key):
        self.model_id = model_id
        self.api_key=api_key
        self.client = self.load()

    def load(self) -> tuple:
       return genai.Client(api_key=self.api_key)

    def rag_answer(self, question_intent: str, processed_question: str, retrieved_context: str) -> str:
        messages = build_prompt(question_intent, processed_question, retrieved_context)
        print('messages', messages)
        return self.generate(messages)

    def generate(self, messages: list[dict]) -> str:
        system_instruction = ""
        contents = []

        for m in messages:
            if m.get('role') == 'system':
                system_instruction = m.get('content', '')
            else:
                role = 'user' if m.get('role') == 'user' else 'model'
                contents.append({
                    "role": role,
                    "parts": [{"text": m.get('content', '')}]
                })

        response = self.client.models.generate_content(
            model=self.model_id,
            config={
                "system_instruction": system_instruction
            },
            contents=contents
        )
        return response.text
                
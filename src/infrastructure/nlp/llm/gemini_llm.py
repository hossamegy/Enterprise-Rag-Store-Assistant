import time
from google import genai
from google.genai import errors as genai_errors
from src.core.ports.local_llm import LocalLLM
from src.core.prompts_templetes.rag_template import build_prompt
from src.config.logger import logger


class LLMUnavailableError(Exception):
    pass

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

    def generate(self, messages: list[dict], max_retries: int = 3, base_delay: float = 2.0) -> str:
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

        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    config={"system_instruction": system_instruction},
                    contents=contents
                )
                return response.text
            except genai_errors.ServerError as e:
                last_error = e
                is_overload = '503' in str(e) or 'UNAVAILABLE' in str(e)
                if is_overload and attempt < max_retries:
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(
                        f'Gemini API unavailable (attempt {attempt}/{max_retries}). '
                        f'Retrying in {delay:.0f}s...'
                    )
                    time.sleep(delay)
                else:
                    break

        raise LLMUnavailableError(
            f'Gemini API remained unavailable after {max_retries} attempts.'
        ) from last_error
                
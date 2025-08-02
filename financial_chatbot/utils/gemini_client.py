import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL
import time
import logging
from langchain.llms.base import LLM
from typing import Optional, List, Any

class GeminiClient:
    def __init__(self,
                temperature: float = 0.3,
                top_p: float = 0.9,
                top_k: int = 40,
                max_output_tokens: int = 1024):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

        self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens
        }
        
        
    def generate_response(self, prompt: str, max_retries: int = 3) -> str:
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                logging.warning(f"Gemini API attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e
                
class GeminiLangChain(LLM):
    """LangChain-compatible wrapper around GeminiClient"""

    def __init__(self, client: Optional[GeminiClient] = None):
        super().__init__()
        self._client = client if client else GeminiClient()

    @property
    def _llm_type(self) -> str:
        return "gemini"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs,
    ) -> str:
        if not hasattr(self, "_client"):
            # Recreate GeminiClient if missing
            self._client = GeminiClient()

        text = self._client.generate_response(prompt)

        if stop:
            for s in stop:
                if s in text:
                    text = text.split(s)[0]
                    break
        return text
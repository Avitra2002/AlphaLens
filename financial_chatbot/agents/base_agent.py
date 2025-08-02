from utils.gemini_client import GeminiClient
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self):
        self.gemini = GeminiClient()
        
    @abstractmethod
    def analyze(self, query: str, company_data: dict, filing_data: str) -> str:
        
        pass
        
    def _create_prompt(self, template: str, **kwargs) -> str:
        
        return template.format(**kwargs)
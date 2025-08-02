from utils.gemini_client import GeminiLangChain
from langchain.prompts import PromptTemplate
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

from config.settings import GEMINI_API_KEY, ROUTER_DESTINATIONS, DEFAULT_INTENT
import logging

from agents.financial_agent import FinancialAgent
from agents.general_agent import GeneralAgent
from agents.relationship_agent import RelationshipAgent
from agents.risk_agent import RiskAgent

class LangChainRouter:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        self.llm = GeminiLangChain()
        self.router_chain = self._create_router_chain()

        # Map intents to agents
        self.destination_agents = {
            "risk_analysis": RiskAgent(),
            "financial_status": FinancialAgent(),
            "relationship_graph": RelationshipAgent(),
            "general_summary": GeneralAgent()
        }

    def _create_router_chain(self) -> LLMRouterChain:
        destinations = [f"{p['name']}: {p['description']}" for p in ROUTER_DESTINATIONS]
        destinations_str = "\n".join(destinations)

        router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
        router_prompt = PromptTemplate(
            template=router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )

        return LLMRouterChain.from_llm(self.llm, router_prompt)

    def classify_intent(self, query: str) -> str:
        try:
            output = self.router_chain.invoke({"input": query})
            return output.get("destination", DEFAULT_INTENT)
        except Exception as e:
            logging.error(f"Intent classification failed: {e}")
            return DEFAULT_INTENT

    def get_agent_for_intent(self, intent: str):
        return self.destination_agents.get(intent, self.destination_agents[DEFAULT_INTENT])

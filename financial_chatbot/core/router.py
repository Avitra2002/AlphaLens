import logging
from core.intent_classifier import LangChainRouter
from core.entity_extractor import EntityExtractor
from api.mapping_api import MappingApi
from api.query_api import QueryApi
from api.extractor_api import ExtractorApi
from config.settings import INTENT_SECTIONS

class Router:
    def __init__(self):
        self.langchain_router = LangChainRouter()
        self.entity_extractor = EntityExtractor()
        self.mapping_api = MappingApi()
        self.query_api = QueryApi()
        self.extractor_api = ExtractorApi()

    def process_query(self, query: str) -> str:
        # Extract company info
        entity_info = self.entity_extractor.extract_company_info(query)
        company_data = self.mapping_api.resolve(entity_info)
        if not company_data:
            return "I couldn't identify the company from your query."

        # Classify intent
        intent = self.langchain_router.classify_intent(query)
        logging.info(f"Predicted intent: {intent}")

        
        sections = INTENT_SECTIONS.get(intent, ['1', '7', '1A'])

        # Fetch filing data for selected sections
        filings = self.query_api.get_filings(company_data)
        if not filings or not filings.get('filings'):
            return f"Could not find recent 10-K filings for {company_data.get('company_name')}."

        filing_url = filings['filings'][0].get('linkToFilingDetails')
        if not filing_url:
            return f"Filing URL not found for {company_data.get('company_name')}."

        filing_data = ""
        for section in sections:
            section_text = self.extractor_api.extract_section(filing_url, section)
            if section_text:
                filing_data += f"\n\n=== {section.upper()} ===\n{section_text}"

        # Get correct agent and analyze
        agent = self.langchain_router.get_agent_for_intent(intent)
        return agent.analyze(query, company_data, filing_data)

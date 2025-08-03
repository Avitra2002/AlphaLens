# core/router.py
import json
import logging
from core.intent_classifier import LangChainRouter
from core.entity_extractor import EntityExtractor
from api.mapping_api import MappingApi
from api.query_api import QueryApi
from api.extractor_api import ExtractorApi
from config.settings import INTENT_SECTIONS
from core.chunker import chunk_text
from core.vector_store import LocalFAISS

class Router:
    def __init__(self):
        self.langchain_router = LangChainRouter()
        self.entity_extractor = EntityExtractor()
        self.mapping_api = MappingApi()
        self.query_api = QueryApi()
        self.extractor_api = ExtractorApi()
        self.vector_store = LocalFAISS()

    def process_query(self, query: str) -> str:
        # Step 1: Extract company info
        entity_info = self.entity_extractor.extract_company_info(query)
        company_data = self.mapping_api.resolve(entity_info)
        print(f"company_data:{company_data}")
        if not company_data:
            return "I couldn't identify the company from your query."

        # Step 2: Classify intent
        intent = self.langchain_router.classify_intent(query)
        print (f'intent:{intent}')
        logging.info(f"Predicted intent: {intent}")
        sections = INTENT_SECTIONS.get(intent, ['1', '7', '1A'])

        # Step 3: Get latest filing
        filings = self.query_api.get_filings(company_data)
        print(f'Filling:{json.dumps(filings, indent=2)[:2000]}')
        if not filings or not filings.get('filings'):
            return f"Could not find recent 10-K filings for {company_data.get('company_name')}."

        latest_filing = filings['filings'][0]
        filing_date = latest_filing.get('filedAt')

        if not filing_date:
            return f"Could not determine filing year for {company_data.get('company_name')}."

        filing_year = filing_date[:4]
        namespace = f"{company_data['ticker']}_{filing_year}_10k"

        # Step 4: Check FAISS cache
        if not self.vector_store.exists(namespace):
            print(f"No FAISS index found for {namespace}. Creating new one...")

            filing_url = filings['filings'][0].get('linkToFilingDetails')
            if not filing_url:
                return f"Filing URL not found for {company_data.get('company_name')}."

            filing_chunks = []
            for section in sections:
                print("fetching from sec api")
                section_text = self.extractor_api.extract_section(filing_url, section)
                if section_text:
                    for chunk_id, chunk in enumerate(chunk_text(section_text, size=2500, overlap=200)):
                        filing_chunks.append({
                            "text": chunk,
                            "metadata": {
                                "company_id": company_data['ticker'],
                                "filing_year": filing_year,
                                "section": section,
                                "chunk_id": chunk_id
                            }
                        })
            if not filing_chunks:
                return f"No relevant sections found in the latest 10-K for {company_data.get('company_name')}."
            self.vector_store.create(namespace, filing_chunks)
        else:
            print(f"FAISS index already exists for {namespace}. Using cache.")


        # Step 5: Route to appropriate agent
        agent = self.langchain_router.get_agent_for_intent(intent)
        # return agent.analyze(query, company_data, context)
        return agent.retrieve_and_analyze(query, company_data, namespace, self.vector_store)

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

        # Step 4: Check FAISS cache & required sections
        missing_sections = []
        if self.vector_store.exists(namespace):
            print(f"FAISS index exists for {namespace}. Checking required sections...")
            existing_sections = self.vector_store.list_sections(namespace)
            for sec in sections:
                if str(sec) not in existing_sections:
                    missing_sections.append(sec)
            print (f"missing sections:{missing_sections}")
        else:
            print(f"No FAISS index found for {namespace}. Creating new one...")
            missing_sections = sections

        # Step 5: Fetch and store missing sections if any
        if missing_sections:
            filing_url = latest_filing.get('linkToFilingDetails')
            if not filing_url:
                return f"Filing URL not found for {company_data.get('company_name')}."

            filing_chunks = []
            for section in missing_sections:
                print(f"Fetching section {section} from SEC API...")
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

            if filing_chunks:
                if self.vector_store.exists(namespace):
                    self.vector_store.add_chunks(namespace, filing_chunks)
                else:
                    self.vector_store.create(namespace, filing_chunks)
            else:
                logging.warning(f"No data fetched for sections {missing_sections} in {company_data.get('company_name')}.")
        else:
            print(f"All required sections already exist for {namespace}.")


        # Step 5: Route to appropriate agent
        agent = self.langchain_router.get_agent_for_intent(intent)
        # return agent.analyze(query, company_data, context)
        raw_results = agent.retrieve_and_analyze(query, company_data, namespace, self.vector_store)

        if isinstance(raw_results, dict) and "relationships" in raw_results:
            data_type = "graph"
        elif isinstance(raw_results, str):
            data_type = "text"
        else:
            data_type = "unknown"
        
        return {
            "intent": intent,
            "company": company_data.get("company_name"),
            "data": raw_results,
            "data_type": data_type,
            "success": True if raw_results else False
        }

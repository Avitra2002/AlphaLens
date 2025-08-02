import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.intent_classifier import LangChainRouter
from api.query_api import QueryApi
from api.extractor_api import ExtractorApi
from config.settings import INTENT_SECTIONS

import logging
logging.basicConfig(level=logging.INFO)

router = LangChainRouter()
qa = QueryApi()
extractor = ExtractorApi()

query = "What is Apple's financial performance?"
company_data = {"company_name": "Apple Inc", "cik": "320193"}

# Classify intent
intent = router.classify_intent(query)
logging.info(f"Predicted intent: {intent}")

sections = INTENT_SECTIONS.get(intent, ['1', '7', '1A'])

logging.info(f"Sections to extract: {sections}")

# Get most recent 10-K filing
filings = qa.get_filings(company_data)
if not filings or not filings.get("filings"):
    print(f"Could not find recent 10-K filings for {company_data['company_name']}.")
    sys.exit()

filing_url = filings["filings"][0].get("linkToFilingDetails")
if not filing_url:
    print(f"Filing URL not found for {company_data['company_name']}.")
    sys.exit()

logging.info(f"Filing URL: {filing_url}")

# Extract sections
filing_data = ""
for section in sections:
    section_text = extractor.extract_section(filing_url, section)
    if section_text:
        filing_data += f"\n\n=== {section.upper()} ===\n{section_text}"
    else:
        filing_data += f"\n\n=== {section.upper()} ===\n[No content found]"

# Print results
print("\n--- Extracted Filing Data ---")
print(filing_data)

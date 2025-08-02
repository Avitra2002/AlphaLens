import requests
import logging
import re
from config.settings import SEC_BASE_URL, SEC_API_KEY

class ExtractorApi:
    def __init__(self):
        self.base_url = f"{SEC_BASE_URL.rstrip('/')}/extractor"
        self.headers = {
            "Authorization": SEC_API_KEY,
            "User-Agent": "Financial Analyzer 1.0"
        }

    def extract_section(self, filing_url: str, item: str, return_type: str = "text") -> str | None:
        try:
            params = {
                "url": filing_url,
                "item": item,
                "type": return_type
            }
            logging.info(f"Extracting item {item} from filing: {filing_url}")
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()

            raw_text = response.text

        
            clean_text = re.sub(r"[^\x20-\x7E\n\r\t]", "", raw_text)

            clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

            return clean_text.strip()

        except Exception as e:
            logging.error(f"Section extraction failed for {item}: {e}")
            return None

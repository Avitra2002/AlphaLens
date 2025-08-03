import requests
import logging
from config.settings import SEC_BASE_URL, SEC_API_KEY

class QueryApi:
    def __init__(self):
        self.base_url = SEC_BASE_URL.rstrip("/")
        self.headers = {
            "Authorization": SEC_API_KEY,
            "User-Agent": "Financial Analyzer 1.0",
            "Content-Type": "application/json"
        }
        
    def get_filings(self, params: dict) -> dict:
        try:
            cik = params.get("cik")
            ticker = params.get("ticker")
            company_name = params.get("company_name")

            # Build query (still try exact match)
            if cik:
                search_query = f'formType:="10-K" AND cik:{cik}'
            elif ticker:
                search_query = f'formType:="10-K" AND ticker:{ticker.upper()}'
            elif company_name:
                search_query = f'formType:="10-K" AND companyName:"{company_name}"'
            else:
                raise ValueError("Must provide cik, ticker, or company_name to get filings")

            payload = {
                "query": search_query,
                "from": "0",
                "size": "3",  # get more results to find the right one
                "sort": [{"filedAt": {"order": "desc"}}]
            }

            url = f"{self.base_url}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()

            filings_list = data.get("filings", [])
            if not filings_list:
                return None

            # Filter to only real 10-K filings (exclude amendments)
            full_10ks = [f for f in filings_list if f.get("formType") == "10-K"]
            if not full_10ks:
                logging.warning("No full 10-K found, all recent filings are amendments")
                return None

            # Take the most recent full 10-K
            chosen_filing = full_10ks[0]

            # Keep same structure for Router
            return {"filings": [chosen_filing]}

        except Exception as e:
            logging.error(f"Filing query failed: {e}")
            return None
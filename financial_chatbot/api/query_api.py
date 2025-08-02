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
        """
        Get company filings using SEC-API Query API.
        Supports cik, ticker, or companyName.
        """
        try:
            cik = params.get("cik")
            ticker = params.get("ticker")
            company_name = params.get("company_name")

            if cik:
                search_query = f'formType:"10-K" AND cik:{cik}'
            elif ticker:
                search_query = f'formType:"10-K" AND ticker:{ticker.upper()}'
            elif company_name:
                search_query = f'formType:"10-K" AND companyName:"{company_name}"'
            else:
                raise ValueError("Must provide cik, ticker, or company_name to get filings")

            payload = {
                "query": search_query,
                "from": "0",
                "size": "1",
                "sort": [{ "filedAt": { "order": "desc" }}]
            }

            url = f"{self.base_url}"
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            logging.error(f"Filing query failed: {e}")
            return None
import requests
import logging
from config.settings import SEC_BASE_URL, SEC_API_KEY
import os
import json
from urllib.parse import quote
class MappingApi:
    def __init__(self):
        self.base_url = SEC_BASE_URL
        self.headers = {
            'Authorization': SEC_API_KEY,
            'User-Agent': 'Financial Analyzer 1.0'
        }
        json_path = os.path.join(os.path.dirname(__file__), "../data/company_tickers.json")
        with open(json_path, "r") as f:
            self.ticker_data = json.load(f)
        
    def resolve(self, entity_info: dict) -> dict:
        #Resolve company info to CIK
        
        ticker = entity_info.get('ticker')
        company = entity_info.get('company')
        
        if ticker:
            return self._resolve_by_ticker(ticker)
        elif company:
            return self._resolve_by_company_name(company)
        else:
            return None
            
    # def _resolve_by_ticker(self, ticker: str) -> dict:
    #     """Resolve ticker to CIK"""
    #     try:
    #         url = f"{self.base_url}/mapper-api"
    #         params = {'ticker': ticker.upper()}
            
    #         response = requests.get(url, params=params, headers=self.headers)
    #         response.raise_for_status()
            
    #         data = response.json()
    #         return {
    #             'ticker': ticker.upper(),
    #             'cik': data.get('cik'),
    #             'company_name': data.get('name')
    #         }
            
    #     except Exception as e:
    #         logging.error(f"Ticker resolution failed for {ticker}: {e}")
    #         return None

    def _resolve_by_ticker(self, ticker: str) -> dict | None:
        #Resolve ticker to CIK using SEC's official JSON
        ticker_upper = ticker.upper()

        for entry in self.ticker_data.values():
            if entry.get("ticker") == ticker_upper:
                return {
                    "ticker": ticker_upper,
                    "cik": str(entry.get("cik_str")).zfill(10),  # pad for EDGAR
                    "company_name": entry.get("title")
                }
        return None
            
    from urllib.parse import quote

    def _resolve_by_company_name(self, company_name: str) -> dict:
        #Resolve company name to CIK using SEC-API.io
        try:
            # URL-encode
            encoded_name = quote(company_name)
            url = f"{self.base_url}/mapping/name/{encoded_name}"

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            data = response.json()

            # The API returns an array of matches — use the first one
            if isinstance(data, list) and data:
                match = data[0]
                return {
                    'ticker': match.get('ticker'),
                    'cik': match.get('cik'),
                    'company_name': match.get('name')
                }

            return None

        except Exception as e:
            logging.error(f"Company name resolution failed for {company_name}: {e}")
            return None

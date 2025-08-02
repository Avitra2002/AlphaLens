from utils.gemini_client import GeminiClient
import re
import logging
from config.settings import ALPHAVANTAGE_API_KEY
import requests
import os
import json
import difflib

class EntityExtractor:
    def __init__(self):
        self.gemini = GeminiClient()
        json_path = os.path.join(os.path.dirname(__file__), "../data/company_tickers.json")
        try:
            with open(json_path, "r") as f:
                self.ticker_data = json.load(f)
        except Exception as e:
            logging.error(f"Could not load SEC ticker JSON: {e}")
            self.ticker_data = {}

        
    def extract_company_info(self, query: str) -> dict:
        
        prompt = f"""
        Extract the company name from this query.
        
        Query: "{query}"
        
        Return in this exact format:
        Company: [company name or "None" if not found]
        """
        
        try:
            response = self.gemini.generate_response(prompt)
            
            # Parse company name from Gemini response
            company_match = re.search(r'Company:\s*(.+)', response)
            company = company_match.group(1).strip("[]\"' \n") if company_match else None

            if company and company.lower() in ['none', 'not found']:
                company = None
            
            ticker = None
            if company:
                ticker = self.get_ticker_for_company(company)
            
            return {
                'company': company,
                'ticker': ticker
            }
            
        except Exception as e:
            logging.error(f"Entity extraction failed: {e}")
            return {'company': None, 'ticker': None}
    
    def get_ticker_for_company(self, company_name: str) -> str | None:
        """Match company name to ticker using SEC company_tickers.json with fuzzy matching."""
        if not company_name or not self.ticker_data:
            return None

        company_name_clean = company_name.lower().replace("inc.", "").strip()

        best_match = None
        max_token_overlap = 0

        for entry in self.ticker_data.values():
            sec_name = entry.get("title", "").lower().replace("inc.", "").strip()
            ticker = entry.get("ticker")

            # Exact or partial match
            if sec_name == company_name_clean or company_name_clean in sec_name:
                return ticker

            # Token overlap
            company_tokens = set(company_name_clean.split())
            sec_tokens = set(sec_name.split())
            token_overlap = len(company_tokens & sec_tokens)

            if token_overlap > max_token_overlap:
                max_token_overlap = token_overlap
                best_match = ticker

        # Fallback: Fuzzy match using difflib
        if not best_match:
            sec_titles = [entry["title"] for entry in self.ticker_data.values()]
            close_matches = difflib.get_close_matches(company_name, sec_titles, n=1, cutoff=0.8)
            if close_matches:
                for entry in self.ticker_data.values():
                    if entry["title"] == close_matches[0]:
                        return entry["ticker"]

        return best_match
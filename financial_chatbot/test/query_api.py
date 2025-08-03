import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.query_api import QueryApi

qa = QueryApi()

# With CIK
print("With CIK")
print(qa.get_filings({"cik": "320193"}))

# # With ticker
# print("\nWith Ticker")
# print(qa.get_filings({"ticker": "AAPL"}))

# # With company name
# print("\nWith Company Name")
# print(qa.get_filings({"company_name": "Apple"}))

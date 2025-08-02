# test_mapping_api.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.mapping_api import MappingApi

mapping = MappingApi()

print ("---Resolve by ticker using json---")
entity_info = {"ticker": "AAPL", "company": 'Apple'}

result = mapping.resolve(entity_info)

print("Test: Resolve by ticker 'AAPL'")
print(result)

print ("--- Resolve by company name using sec-api---")
entity_info = {"ticker": None, "company": "Apple"}

result = mapping.resolve(entity_info)
print("Test: Resolve by company 'Apple'")
print(result)
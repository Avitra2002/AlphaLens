import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.entity_extractor import EntityExtractor

ee = EntityExtractor()
print(ee.extract_company_info("Tell me about Apple's financial status"))

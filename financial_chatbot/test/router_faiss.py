import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.router import Router

router = Router()
print(router.process_query("How is Tesla's market?"))
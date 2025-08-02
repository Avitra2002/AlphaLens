import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = 'gemini-1.5-pro'
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')

# SEC API Configuration
SEC_BASE_URL = 'https://api.sec-api.io'
SEC_API_KEY = os.getenv('SEC_API_KEY', '')

# Rate limiting
MAX_RETRIES = 3
RETRY_DELAY = 1

# Intent classification
INTENTS = [
    'financial_status',
    'relationship_graph', 
    'risk_analysis',
    'general_summary'
]

INTENT_SECTIONS = {
    "financial_status": ['7', '8'],
    "relationship_graph": ['1', '2'],
    "risk_analysis": ['1A'],
    "general_summary": ['1', '7']
}
DEFAULT_INTENT = 'general_summary'

# LangChain Router Configuration
ROUTER_DESTINATIONS = [
    {
        "name": "financial_status",
        "description": "Good for answering questions about company financial performance, revenue, profits, financial metrics, and financial health"
    },
    {
        "name": "relationship_graph", 
        "description": "Good for answering questions about company relationships, subsidiaries, partnerships, investments, and corporate structure"
    },
    {
        "name": "risk_analysis",
        "description": "Good for answering questions about company risks, threats, challenges, and risk factors"
    },
    {
        "name": "general_summary",
        "description": "Good for general questions about companies and broad business overviews"
    }
]
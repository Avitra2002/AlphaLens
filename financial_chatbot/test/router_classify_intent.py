import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.intent_classifier import LangChainRouter

router = LangChainRouter()

query = "Tell me about Tesla's risk factors"
intent = router.classify_intent(query)
print(f"Predicted intent: {intent}")

agent = router.get_agent_for_intent(intent)
print(f"Selected agent: {agent.__class__.__name__}")

query = "What companies are related to Tesla"
intent = router.classify_intent(query)
print(f"Predicted intent: {intent}")

agent = router.get_agent_for_intent(intent)
print(f"Selected agent: {agent.__class__.__name__}")
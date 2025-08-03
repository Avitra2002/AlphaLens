import logging
from typing import List
from dataclasses import dataclass
from utils.gemini_client import GeminiClient
import re

@dataclass
class RelationshipSchema:
    entity1: str
    entity2: str
    relationship_type: str
    confidence: float
    context: str


GENERIC_TERMS = {
    "subsidiaries", "customers", "partners", "shareholders", "employees", "stakeholders"
}

def normalize_company_name(name: str) -> str:
    if not name:
        return ""
    name = name.lower()
    # Remove punctuation
    name = re.sub(r"[^\w\s]", "", name)
    # Remove common corporate suffixes
    suffixes = ["inc", "incorporated", "corp", "corporation", "ltd", "limited", "llc", "plc"]
    words = [w for w in name.split() if w not in suffixes]
    return " ".join(words).title()

def is_generic_entity(name: str) -> bool:
    return name.lower().strip() in GENERIC_TERMS

def extract_relationships_gemini(query, sentences: List[str], company_name: str) -> List[RelationshipSchema]:
    # Extract relationships from a list of sentences using Gemini function-calling style prompts.
    gemini = GeminiClient()
    relationships: List[RelationshipSchema] = []

    if not sentences:
        return relationships

    logging.info(f"Extracting relationships from {len(sentences)} sentences...")

    # Process in batches to avoid overly long prompts
    batch_size = 10
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i + batch_size]

        prompt = f"""
            User Query: {query}

            You are an expert at extracting **real** business relationships from SEC 10-K filings.

            Rules:
            1. Only use relationships explicitly mentioned in the provided sentences.
                - The relationship must be stated directly in the same sentence.
                - Do not assume or infer a relationship based on past associations, individual employment history, or indirect context.
                - For acquisitions, the buyer or seller must be clearly named in the sentence.

            2. If the target company is not the subject or object of the relationship verb 
            (e.g., "acquires", "partners with", "merges with"), do not return it.
            3. Ignore relationships between unrelated third parties (e.g., Google ↔ Fitbit) unless they are directly connected to {company_name}.
            4. Allowed relationship types:
            - partnership
            - subsidiary
            - competitor
            - supplier
            - acquisition
            - joint venture
            - regulatory
            5. Each relationship must be supported by text evidence from the given sentence. Use your knowledge to infere the relationship if its not clear.
            6. Do not include products, services, or generic terms (e.g., customers, competitors) unless tied to another named organization.

            "Do not return relationships where both entity1 and entity2 are unrelated to {company_name}."

            Return the results in strict JSON format:
            [
            {{
                "entity1": "...",
                "entity2": "...",
                "relationship_type": "...",
                "confidence": (a float),
                "context": "..."
            }}
            ]

            Sentences:
            {chr(10).join(batch)}
            """

        try:
            response_text = gemini.generate_response(prompt)
            extracted = _safe_parse_json(response_text)

            if extracted:
                for rel in extracted:
                    try:
                        e1 = normalize_company_name(rel.get("entity1", ""))
                        e2 = normalize_company_name(rel.get("entity2", ""))

                        # Skip generic placeholder entities
                        if is_generic_entity(e1) or is_generic_entity(e2):
                            continue

                        relationships.append(
                            RelationshipSchema(
                                entity1=e1,
                                entity2=e2,
                                relationship_type=rel.get("relationship_type", "other"),
                                confidence=float(rel.get("confidence", 0.5)),
                                context=rel.get("context", "").strip()
                            )
                        )
                    except Exception as parse_error:
                        print(f"Error parsing relationship object: {parse_error}")
                        continue

        except Exception as e:
            print(f"Error extracting relationships with Gemini: {e}")
            continue
    
    def entity_matches_company(entity: str) -> bool:
        e = entity.lower()
        return company_lower in e or e in company_lower
    
    print (f'relationships before filtering:{relationships}')
    company_lower = company_name.lower()
    relationships= [r for r in relationships if entity_matches_company(r.entity1) or entity_matches_company(r.entity2)]

    unique = {}
    for r in relationships:
        key = (
            r.entity1.lower().strip(),
            r.entity2.lower().strip(),
            r.relationship_type.lower().strip()
        )
        # Keep the first occurrence only
        if key not in unique:
            unique[key] = r

    relationships = list(unique.values())

    print(f"Extracted {len(relationships)} relationships.")
    print(f'eg relationships extracted: {relationships[:5]}')
    return relationships 

def _safe_parse_json(text: str):
    import json
    try:
       
        if text.strip().startswith("```"):
            text = text.strip().strip("`")
            
            if text.lower().startswith("json"):
                text = text[4:].strip()

        return json.loads(text)
    except Exception as e:
        logging.warning(f"Failed to parse JSON from Gemini output: {e}")
        return None

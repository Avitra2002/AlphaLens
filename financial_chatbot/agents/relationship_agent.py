from agents.base_agent import BaseAgent
from config.settings import INTENT_SECTIONS
import re
import spacy
from typing import List
from utils.relationship_extractor_gemini import extract_relationships_gemini
import feedparser
from utils.save_to_neo4j import save_to_neo4j

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

class RelationshipAgent(BaseAgent):
    def fetch_google_news_sentences(self, company_name: str,user_query: str, max_results: int = 10) -> List[str]:

        #Fetch latest Google News headlines & summaries for the company,
        
        relationship_keywords = [
            "partnership", "partners with", "acquisition", "acquires",
            "merger", "invests in", "investment", "joint venture", 
            "collaboration", "alliance"
        ]
        if user_query:
            search_terms = f"{company_name} {user_query}"
        else:
            search_terms = f"{company_name} ({' OR '.join(relationship_keywords)})"

        query = search_terms.replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(url)

        sentences = []
        for entry in feed.entries[:max_results]:
            text = entry.title
            if hasattr(entry, "summary"):
                text += f". {entry.summary}"
            sentences.append(text.strip())

        print(f"[Google News] Retrieved {len(sentences)} relationship-related news items for {company_name}")
        print (f"Google News sentences:{sentences}")
        return sentences
    

    def filter_company_related_sentences(self, sentences: List[str], company_name: str) -> List[str]:
        company_lower = company_name.lower()
        return [s for s in sentences if company_lower in s.lower()]
    
    def retrieve_and_analyze(self, query, company_data, namespace, vector_store):

        sections = INTENT_SECTIONS.get("relationship_graph", [])

        # ----IF USE ALL CHUNKS-----
        all_chunks = []
        for sec in sections:
            section_chunks = vector_store.get_chunks_by_section(namespace, sec)
            all_chunks.extend(section_chunks)

        if not all_chunks:
            return f"No relevant sections {sections} found for {company_data.get('company_name')}."

        print(f"Retrieved {len(all_chunks)} chunks for relationship analysis.")

        # ------TOP N CHUNCKS-----------
        # relevant_chunks = vector_store.search(
        #     namespace=namespace,
        #     query=query,
        #     top_k=12, 
        #     filter_sections=sections
        # )

        # if not relevant_chunks:
        #     return f"No relevant sections {sections} found for {company_data.get('company_name')}."

        # print(f"Retrieved {len(relevant_chunks)} chunks for relationship analysis.")
        #------------------------------

        # Extract candidate sentences with ≥2 named entities
        candidate_sentences = []
        for chunk in all_chunks:
            candidate_sentences.extend(self.extract_candidate_sentences(chunk["text"]))

        print(f"Extracted {len(candidate_sentences)} candidate sentences with multiple named entities.")

        if not candidate_sentences:
            return f"No relationship-relevant sentences found for {company_data.get('company_name')}."
        
        filtered_sentences = self.filter_company_related_sentences(candidate_sentences, company_data["company_name"])
        print(f"Filtered to {len(filtered_sentences)} sentences mentioning {company_data['company_name']}.")


        news_sentences = self.fetch_google_news_sentences(company_data["company_name"], user_query=query)
        print(f"Fetched {len(news_sentences)} additional news sentences for relationship analysis.")

        combined_sentences = list(set(filtered_sentences + news_sentences))

        if not combined_sentences:
            return f"No company-related relationship sentences found for {company_data.get('company_name')}."

        # Use Gemini function calling
        relationships = extract_relationships_gemini(query,combined_sentences, company_data["company_name"])

        return self.analyze(query, company_data, relationships)
    
    def extract_candidate_sentences(self, text: str):
        text = self.clean_text(text)
        doc = nlp(text[:1_000_000]) 
        candidate_sentences = []
        for sent in doc.sents:
            ents = [ent for ent in sent.ents if ent.label_ in ["ORG"]]
            if len(ents) >= 2:
                candidate_sentences.append(sent.text.strip())
        print (f"Important Sentences:{candidate_sentences}")
        return candidate_sentences

    def clean_text(self, text: str):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', ' ', text)
        return text.strip()


    
    def analyze(self, query: str, company_data: dict, relationships):
        if not relationships:
            return {
                "relationships": [],
                "summary": f"No relationships found for {company_data.get('company_name')}.",
                "data_type": "graph"
            }

        # Save to Neo4j
        save_to_neo4j(relationships)

        summary_lines = [f"**Business Relationships for {company_data.get('company_name')}**\n"]
        for rel in relationships:
            summary_lines.append(
                f"- **{rel.entity1}** ↔ **{rel.entity2}**: {rel.relationship_type} "
                f"(confidence: {rel.confidence:.2f})"
            )

       
        return {
            "relationships": [
                {
                    "entity1": rel.entity1,
                    "entity2": rel.entity2,
                    "relationship_type": rel.relationship_type,
                    "confidence": rel.confidence,
                    "context": rel.context  # include context for tooltip/hover UI
                }
                for rel in relationships
            ],
            "summary": "\n".join(summary_lines),
        }
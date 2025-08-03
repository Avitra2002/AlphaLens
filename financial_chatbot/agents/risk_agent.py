from agents.base_agent import BaseAgent
from config.settings import INTENT_SECTIONS

class RiskAgent(BaseAgent):
    def retrieve_and_analyze(self, query, company_data, namespace, vector_store):
        sections= INTENT_SECTIONS.get("risk_analysis",[])
        all_chunks = []

        for sec in sections:
            section_chuncks= vector_store.get_chunks_by_section(namespace, sec)
            all_chunks.extend(section_chuncks)

        # Summarize each chunk 
        print('summary by chunks')
        summaries = []
        for chunk in all_chunks:
            if chunk["text"].strip():
                prompt = f"Summarize the following risk factors:\n\n{chunk['text']}"
                summaries.append(self.gemini.generate_response(prompt))

        summarized_text = "\n".join(summaries)
        return self.analyze(query, company_data, summarized_text)

    
    def analyze(self, query: str, company_data: dict, filing_data: str) -> str:
        """Analyze company risks"""
        
        template = """
        You are a risk analysis assistant. Analyze the following 10-K risk factors section and summarize the key risks facing the company.

        Company: {company_name}
        User Question: {query}

        Risk Factors Section:
        {filing_data}

        Summarize the main risks in categories such as:
        - Market and competitive risks
        - Operational risks
        - Financial risks

        Provide a clear, organized summary of the most significant risks.

        Response:
        """
        
        prompt = self._create_prompt(
            template,
            company_name=company_data.get('company_name', 'Unknown'),
            query=query,
            filing_data=filing_data[:4000]
        )
        
        return self.gemini.generate_response(prompt)
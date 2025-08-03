from agents.base_agent import BaseAgent
from config.settings import INTENT_SECTIONS

class FinancialAgent(BaseAgent):
    def retrieve_and_analyze(self, query, company_data, namespace, vector_store):

        sections = INTENT_SECTIONS.get("financial_status", [])
        all_chunks = []
        for sec in sections:
            section_chunks = vector_store.get_chunks_by_section(namespace, sec)
            all_chunks.extend(section_chunks)

        if not all_chunks:
            return f"No relevant sections ({sections}) found for {company_data.get('company_name')}."
        
        # Summarize each chunk
        summaries = []
        print('summary by chunk')
        for chunk in all_chunks:
            prompt = f"Summarize the following financial discussion:\n\n{chunk['text']}"
            summaries.append(self.gemini.generate_response(prompt))

        combined_summary = "\n".join(summaries)
        return self.analyze(query, company_data, combined_summary)
    
    def analyze(self, query: str, company_data: dict, filing_data: str) -> str:
        """Analyze financial status"""
        
        template = """
        You are a financial analysis assistant. Analyze the following 10-K filing data and answer the user's question about the company's financial status.

        Company: {company_name}
        User Question: {query}

        10-K Filing Data:
        {filing_data}

        Provide a clear, concise analysis focusing on:
        - Key financial metrics and performance
        - Revenue trends and profitability
        - Financial health indicators
        - Important financial highlights

        Response:
        """
        
        prompt = self._create_prompt(
            template,
            company_name=company_data.get('company_name', 'Unknown'),
            query=query,
            filing_data=filing_data[:4000]  # Limit text for API
        )
        
        return self.gemini.generate_response(prompt)
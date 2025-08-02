from agents.base_agent import BaseAgent

class GeneralAgent(BaseAgent):
    def analyze(self, query: str, company_data: dict, filing_data: str) -> str:
        """Provide general company analysis"""
        
        template = """
        You are a general business analysis assistant. Provide a comprehensive overview of the company based on the following 10-K filing data.

        Company: {company_name}
        User Question: {query}

        10-K Filing Data (Business and MD&A sections):
        {filing_data}

        Provide a well-rounded summary covering:
        - What the company does (business model)
        - Key business segments and operations
        - Recent performance highlights
        - Market position and competitive landscape

        Response:
        """
        
        prompt = self._create_prompt(
            template,
            company_name=company_data.get('company_name', 'Unknown'),
            query=query,
            filing_data=filing_data[:4000]
        )
        
        return self.gemini.generate_response(prompt)
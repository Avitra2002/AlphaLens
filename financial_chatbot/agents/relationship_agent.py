from agents.base_agent import BaseAgent

class RelationshipAgent(BaseAgent):
    def analyze(self, query: str, company_data: dict, filing_data: str) -> str:
        """Analyze company relationships"""
        
        template = """
        You are a relationship analysis assistant. Analyze the following 10-K filing data to identify company relationships, subsidiaries, partnerships, and investments.

        Company: {company_name}
        User Question: {query}

        10-K Filing Data (Business section and subsidiaries):
        {filing_data}

        Focus on identifying:
        - Subsidiaries and controlled companies
        - Joint ventures and partnerships
        - Major investments and holdings
        - Strategic relationships

        Present the relationships in a clear, organized manner.

        Response:
        """
        
        prompt = self._create_prompt(
            template,
            company_name=company_data.get('company_name', 'Unknown'),
            query=query,
            filing_data=filing_data[:4000]
        )
        
        return self.gemini.generate_response(prompt)
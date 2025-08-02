from agents.base_agent import BaseAgent

class FinancialAgent(BaseAgent):
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
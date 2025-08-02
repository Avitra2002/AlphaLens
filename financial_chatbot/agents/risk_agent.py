from agents.base_agent import BaseAgent

class RiskAgent(BaseAgent):
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
        - Regulatory and compliance risks
        - Technology and cybersecurity risks

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
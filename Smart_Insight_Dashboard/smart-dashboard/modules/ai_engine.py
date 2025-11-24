import openai
import os
from .utils import logger

class AIEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        else:
            logger.warning("No OpenAI API Key found. AI features will be disabled.")

    def generate_insight(self, context, prompt_type='executive_summary'):
        """Generate insights using OpenAI."""
        if not self.api_key:
            return "AI Insights unavailable. Please provide an OpenAI API Key."

        prompts = {
            'executive_summary': f"Analyze this sales data summary and provide a concise executive summary for stakeholders: {context}",
            'trend_summary': f"Analyze these sales trends and identify key patterns: {context}",
            'region_performance': f"Compare regional performance and suggest improvements: {context}",
            'anomaly_detection': f"Identify any anomalies or outliers in this data: {context}",
            'forecast_interpretation': f"Interpret this sales forecast and potential risks: {context}",
            'category_insights': f"Provide insights on product category performance: {context}",
            'discount_causality': f"Analyze the relationship between discounts and sales volume/profit: {context}",
            'rfm_segment': f"Suggest marketing strategies for these customer segments: {context}",
            'growth_explanation': f"Explain the Month-over-Month and Year-over-Year growth figures: {context}",
            'root_cause': f"Hypothesize root causes for the observed performance dips: {context}"
        }
        
        prompt = prompts.get(prompt_type, prompts['executive_summary'])
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a senior data analyst providing business insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return f"Error generating insight: {str(e)}"

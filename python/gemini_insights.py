import os
from typing import Dict, Any

import google.generativeai as genai


def configure_gemini(api_key: str | None = None) -> None:
    key = api_key or os.getenv('GEMINI_API_KEY')
    if not key:
        raise ValueError('GEMINI_API_KEY is not set.')
    genai.configure(api_key=key)


def generate_business_report(metrics: Dict[str, Any]) -> str:
    configure_gemini()
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    You are a business analyst. Analyze the following retail metrics and generate:
    1. Executive Summary
    2. Key Insights
    3. Sales Trends
    4. Customer Behavior
    5. Business Recommendations
    6. Opportunities for Growth

    Metrics:
    {metrics}
    """
    response = model.generate_content(prompt)
    return response.text

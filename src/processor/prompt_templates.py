from datetime import datetime
import json
from typing import List, Dict

SYSTEM_PROMPT = """You are a precise JSON generator that converts business metric queries into structured data. Always respond with valid JSON objects matching the exact structure shown in examples. Never include additional text or explanations."""

def format_user_prompt(query: str, history: List[Dict]) -> str:
    """
    Format the user prompt with examples and context.
    Returns a non-empty string suitable for the Groq API.
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    context = ""
    if history and any(word in query.lower() for word in ['this', 'that', 'compare', 'them', 'it']):
        last_query = history[-1]
        context = f"""
            Previous query: "{last_query['query']}"
            Previous response: {json.dumps(last_query['response'])}

            For follow-up queries:
            - Include ALL entities being compared (previous and new)
            - Maintain the exact same parameter as the previous query
            - Use the same date range as the previous query
        """

    template = f"""
        You are a JSON generator that converts business metric queries into structured data.

        Current date: {today}

        {context}

        Instructions:
        1. Extract company names, metrics, and date ranges from queries
        2. Convert all dates to YYYY-MM-DD format
        3. If dates aren't specified:
          - "last quarter" = most recent completed quarter
          - "this year" = January 1st to today
          - "last year" = previous calendar year
          - "last month" = most recent completed month
          - "last year" or "last 1 year" = one year ago until today
        4. For comparison queries using words like "this", "that", or "compare":
          - Include ALL entities being compared in the response
          - Always use the EXACT same parameter as the previous query
          - Use the EXACT same date range as the previous query
        5. Return ONLY the JSON object, no other text

        Example queries and their responses:

        Query: "Get me Flipkart's GMV for the last one year"
        {{"entities": ["Flipkart"], "parameter": "GMV", "start_date": "2023-01-07", "end_date": "2024-01-07"}}

        Query: "Compare this with Amazon"
        {{"entities": ["Flipkart", "Amazon"], "parameter": "GMV", "start_date": "2023-01-07", "end_date": "2024-01-07"}}

        Now process this query:
        {query}
    """
    
    return template.strip()

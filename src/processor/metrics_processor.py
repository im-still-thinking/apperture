from typing import List, Dict
import groq
import json
from ..lib.date_utils import validate_date_format
from .prompt_templates import SYSTEM_PROMPT, format_user_prompt

class MetricsProcessor:
    def __init__(self, api_key: str):
        """Initialize the processor with Groq API credentials."""

        self.client = groq.Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"
        self.history: List[Dict] = []
        self.history_length = 6

    def process_query(self, query: str) -> List[Dict]:
        """Process a user query and return structured JSON output."""
        try:

            user_prompt = format_user_prompt(query, self.history)
            if not user_prompt:
                raise ValueError("Failed to generate valid prompt")

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=500
            )

            response_text = response.choices[0].message.content.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:-3]
            elif response_text.startswith('```'):
                response_text = response_text[3:-3]
                
            extracted_info = json.loads(response_text.strip())
            
            if any(word in query.lower() for word in ['this', 'that', 'compare', 'them', 'it']) and self.history:
                last_query = self.history[-1]['response'][0]
                
                if last_query["entity"] not in extracted_info["entities"]:
                    extracted_info["entities"].insert(0, last_query["entity"])
                extracted_info["parameter"] = last_query["parameter"]
                extracted_info["start_date"] = last_query["start_date"]
                extracted_info["end_date"] = last_query["end_date"]
            
            start_date = validate_date_format(extracted_info["start_date"])
            end_date = validate_date_format(extracted_info["end_date"])
            
            if not start_date or not end_date:
                raise ValueError("Invalid date format in LLM response")
                
            result = []
            for entity in extracted_info["entities"]:
                result.append({
                    "entity": entity,
                    "parameter": extracted_info["parameter"],
                    "start_date": start_date,
                    "end_date": end_date
                })
            
            self.history.append({
                "query": query,
                "response": result
            })
            if len(self.history) > self.history_length:
                self.history.pop(0)
                
            return result
            
        except json.JSONDecodeError as e:
            print(f"Raw LLM response: {response_text if 'response_text' in locals() else 'No response'}")
            return [{
                "error": "Failed to parse LLM response",
                "details": f"Invalid JSON format: {str(e)}"
            }]
        except Exception as e:
            return [{
                "error": "Failed to process query",
                "details": str(e)
            }]
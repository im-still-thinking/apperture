from typing import Optional
from dateutil import parser

def validate_date_format(date_str: str) -> Optional[str]:
    """Validate that a date string is in YYYY-MM-DD format."""
    try:
        parsed_date = parser.parse(date_str)
        return parsed_date.strftime("%Y-%m-%d")
    except:
        return None
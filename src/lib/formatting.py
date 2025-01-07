import pandas as pd
from typing import List, Dict

def format_response_as_table(response: List[Dict]) -> pd.DataFrame:
    """Convert the response into a pandas DataFrame for table display."""
    return pd.DataFrame(response).rename(columns={
        "entity": "Company",
        "parameter": "Metric",
        "start_date": "Start Date",
        "end_date": "End Date"
    })
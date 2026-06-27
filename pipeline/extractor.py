import re

def extract_codes(text: str) -> dict:
    """
    Deterministic extraction of CPT codes and key fields.
    Returns a dict keyed by code number.
    """
    codes = {}
    # Match patterns like "99213 - Office visit, established patient"
    # Adjust regex to match your actual PDF format
    pattern = re.compile(r'\b(\d{5})\b.*?(\$[\d,.]+|\d+\s*unit)', re.IGNORECASE)
    
    for match in pattern.finditer(text):
        code = match.group(1)
        detail = match.group(0)
        codes[code] = {"raw_line": detail}
    
    return codes
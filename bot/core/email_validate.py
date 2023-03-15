import re

def is_valid_email(email):
    """Returns True if email is valid, else False."""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(pattern, email) is not None
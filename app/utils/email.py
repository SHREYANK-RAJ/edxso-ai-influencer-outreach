import re
EMAIL_RE = re.compile(r"(?i)(?<![\w.+-])([a-z0-9][a-z0-9._%+-]{0,63}@[a-z0-9.-]+\.[a-z]{2,})(?![\w.-])")

def extract_public_email(text: str) -> str:
    if not text:
        return "Not Found"
    text = text.replace("[at]", "@").replace("(at)", "@")
    m = EMAIL_RE.search(text)
    return m.group(1) if m else "Not Found"

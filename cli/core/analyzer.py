
def analyze_text(text: str) -> list:
    issues = []
    stripped = text.strip()
    word_count = len(stripped.split())

    if len(stripped) < 50:
        issues.append("Too short (under 50 chars)")

    if len(stripped) > 2000:
        issues.append("Too long (over 2000 chars)")

    if word_count < 5:
        issues.append("Too vague — fewer than 5 words")

    lower = stripped.lower()

    if "summarize" in lower and not any(w in lower for w in ["bullet", "points", "list", "format", "structure"]):
        issues.append("Vague summarization — no output format specified")

    if "write" in lower and word_count < 8:
        issues.append("Unclear write instruction — too few words")

    if any(w in lower for w in ["do this", "do that", "make it", "fix it"]) and word_count < 10:
        issues.append("Vague instruction — missing context")

    return issues

import re

_NOISE = ("shop and learn", "apple footer", "more from apple newsroom", "press contacts",
          "investor relations contact", "follow us", "cookie", "privacy policy", "terms of use",
          "site map", "united states", "choose your country")

def clean_text(text: str, max_chars: int = 420) -> str:
    """Turn raw scraped web content into a short readable excerpt. Never invents text."""
    if not text:
        return ""
    t = text.replace("\r", " ").replace("\n", " ")
    t = re.sub(r"\|[^|]*\|", " ", t)            # drop markdown table rows
    t = re.sub(r"#{1,6}\s*", "", t)              # drop heading markers
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)  # links -> text
    t = re.sub(r"[*_`>]+", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    low = t.lower()
    for marker in _NOISE:  # cut footer/nav tails
        i = low.find(marker)
        if i >= 20:
            t = t[:i].strip()
            break
    if len(t) <= max_chars:
        return t
    cut = t[:max_chars]
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    return (cut[: end + 1] if end > 120 else cut.rstrip() + "…")

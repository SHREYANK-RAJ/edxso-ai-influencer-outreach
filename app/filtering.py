from app.models import Influencer
from app.config import settings

TECH_TERMS = {"technology","tech","gadget","gadgets","smartphone","mobile","ai",
"artificial intelligence","software","developer","coding","laptop","camera","apps",
"electronics","programming"}

def relevance_score(i: Influencer) -> int:
    text = " ".join([i.category, i.bio, *i.content_themes, *i.recent_content]).lower()
    return sum(1 for t in TECH_TERMS if t in text)

def qualify(i: Influencer) -> Influencer:
    reasons = []
    ok = True
    if i.followers is None:
        ok = False; reasons.append("Follower count unavailable")
    elif not settings.min_followers <= i.followers <= settings.max_followers:
        ok = False; reasons.append(f"Follower count outside {settings.min_followers:,}–{settings.max_followers:,}")
    if relevance_score(i) < 1:
        ok = False; reasons.append("Insufficient technology/gadget relevance")
    if i.engagement_rate is None:
        ok = False; reasons.append("Engagement rate unavailable")
    elif i.engagement_rate < settings.min_engagement_rate:
        ok = False; reasons.append(f"Engagement rate below {settings.min_engagement_rate}%")
    if i.email == "Not Found":
        ok = False; reasons.append("Public contact email not found")
    i.qualified = ok
    i.filter_reasons = ["Qualified"] if ok else reasons
    return i

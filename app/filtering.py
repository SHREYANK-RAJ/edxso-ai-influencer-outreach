from app.models import Influencer
from app.config import settings

TECH_TERMS = {"technology","tech","gadget","gadgets","smartphone","mobile","ai",
"artificial intelligence","software","developer","coding","laptop","camera","apps",
"electronics","programming"}

<<<<<<< HEAD
def _target_terms() -> set[str]:
    target = settings.target_niche.strip().lower()
    terms = {target, *[word for word in target.replace("/", " ").split() if len(word) > 1]}
    if target in {"technology", "tech", "gadgets", "technology/gadgets"}:
        terms.update(TECH_TERMS)
    return terms


def relevance_score(i: Influencer) -> int:
    text = " ".join([i.category, i.bio, *i.content_themes, *i.recent_content]).lower()
    return sum(1 for term in _target_terms() if term in text)
=======
def relevance_score(i: Influencer) -> int:
    text = " ".join([i.category, i.bio, *i.content_themes, *i.recent_content]).lower()
    return sum(1 for t in TECH_TERMS if t in text)
>>>>>>> origin/main

def qualify(i: Influencer) -> Influencer:
    reasons = []
    ok = True
    if i.followers is None:
        ok = False; reasons.append("Follower count unavailable")
<<<<<<< HEAD
    elif i.followers < settings.min_followers:
        ok = False; reasons.append(f"Follower count below minimum of {settings.min_followers:,}")
    elif i.followers > settings.max_followers:
        ok = False; reasons.append(f"Follower count above maximum of {settings.max_followers:,}")
    if relevance_score(i) < 1:
        ok = False; reasons.append(f"Insufficient relevance to target niche: {settings.target_niche}")
=======
    elif not settings.min_followers <= i.followers <= settings.max_followers:
        ok = False; reasons.append(f"Follower count outside {settings.min_followers:,}–{settings.max_followers:,}")
    if relevance_score(i) < 1:
        ok = False; reasons.append("Insufficient technology/gadget relevance")
>>>>>>> origin/main
    if i.engagement_rate is None:
        ok = False; reasons.append("Engagement rate unavailable")
    elif i.engagement_rate < settings.min_engagement_rate:
        ok = False; reasons.append(f"Engagement rate below {settings.min_engagement_rate}%")
    if i.email == "Not Found":
        ok = False; reasons.append("Public contact email not found")
    i.qualified = ok
    i.filter_reasons = ["Qualified"] if ok else reasons
    return i

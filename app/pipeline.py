import csv
from dataclasses import asdict
from pathlib import Path
from app.discovery.youtube import YouTubeDiscovery
from app.filtering import qualify
from app.models import Influencer
from app.personalization.llm import Personalizer
from app.sending.service import OutreachService
from app.storage.db import OutreachDB
from app.config import settings

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"


def load_seed(path=DATA_DIR / "discovered_seed_50.csv"):
    items = []
    with Path(path).open(encoding="utf-8") as file:
        for row in csv.DictReader(file):
            engagement = row["engagement_rate"]
            items.append(Influencer(
                name=row["name"], platform=row["platform"], profile_url=row["profile_url"],
                followers=int(row["followers"]) if row["followers"] else None,
                engagement_rate=float(engagement.rstrip("%")) if engagement not in ("Not Available", "") else None,
                category=row["niche"], content_themes=[row["content_theme"]], email=row["email"],
                geography=row["geography"], source=row["source"], source_url=row["source_url"],
            ))
    return items

def save_csv(items, path):
    if not items: return
    rows=[]
    for i in items:
        r=asdict(i)
        r["content_themes"]="; ".join(i.content_themes)
        r["recent_content"]=" | ".join(i.recent_content)
        r["filter_reasons"]="; ".join(i.filter_reasons)
        rows.append(r)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

def run_seed():
    return [qualify(item) for item in load_seed()]


def run_live(query=None, limit=50):
    d=YouTubeDiscovery()
    items=[]
    for c in d.discover(query or settings.target_niche, limit):
        enrichment_error = None
        try:
            c = d.enrich_engagement(c)
        except Exception as exc:
            enrichment_error = f"Engagement enrichment failed: {type(exc).__name__}"
        c = qualify(c)
        if enrichment_error:
            c.filter_reasons.append(enrichment_error)
        items.append(c)
    save_csv(items, DATA_DIR / "runtime_discovered.csv")
    return items

def personalize_qualified(items):
    p=Personalizer()
    for i in items:
        if i.qualified:
            try:
                p.generate(i)
            except Exception as exc:
                i.filter_reasons.append(f"Personalization failed: {type(exc).__name__}")
    save_csv(items, DATA_DIR / "runtime_personalized.csv")
    return items

def send_qualified(items,dry_run=True):
    service=OutreachService(OutreachDB())
    return [(i,service.send_email(i,dry_run)) for i in items if i.qualified]

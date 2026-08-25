import csv
from dataclasses import asdict
from app.discovery.youtube import YouTubeDiscovery
from app.filtering import qualify
from app.personalization.llm import Personalizer
from app.sending.service import OutreachService
from app.storage.db import OutreachDB
from app.config import settings

def save_csv(items, path):
    if not items: return
    rows=[]
    for i in items:
        r=asdict(i)
        r["content_themes"]="; ".join(i.content_themes)
        r["recent_content"]=" | ".join(i.recent_content)
        r["filter_reasons"]="; ".join(i.filter_reasons)
        rows.append(r)
    with open(path,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

def run_live(limit=50):
    d=YouTubeDiscovery()
    items=[]
    for c in d.discover(settings.target_niche,limit):
        try: c=d.enrich_engagement(c)
        except Exception as e: c.filter_reasons=[f"Enrichment failed: {type(e).__name__}"]
        items.append(qualify(c))
    save_csv(items,"data/runtime_discovered.csv")
    return items

def personalize_qualified(items):
    p=Personalizer()
    for i in items:
        if i.qualified: p.generate(i)
    save_csv(items,"data/runtime_personalized.csv")
    return items

def send_qualified(items,dry_run=True):
    service=OutreachService(OutreachDB())
    return [(i,service.send_email(i,dry_run)) for i in items if i.qualified]

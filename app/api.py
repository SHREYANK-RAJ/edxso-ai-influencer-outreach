from fastapi import FastAPI
from pathlib import Path
import csv

app=FastAPI(title="Edxso Influencer Outreach API",version="1.0.0")

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/influencers")
def influencers():
    p=Path("data/runtime_personalized.csv")
    if not p.exists(): p=Path("data/discovered_seed_50.csv")
    with p.open(encoding="utf-8") as f: return list(csv.DictReader(f))

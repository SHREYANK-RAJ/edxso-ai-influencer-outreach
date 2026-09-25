from fastapi import FastAPI
from pathlib import Path
import csv

app=FastAPI(title="Edxso Influencer Outreach API",version="1.0.0")
<<<<<<< HEAD
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
=======
>>>>>>> origin/main

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/influencers")
def influencers():
<<<<<<< HEAD
    p=DATA_DIR / "runtime_personalized.csv"
    if not p.exists(): p=DATA_DIR / "discovered_seed_50.csv"
=======
    p=Path("data/runtime_personalized.csv")
    if not p.exists(): p=Path("data/discovered_seed_50.csv")
>>>>>>> origin/main
    with p.open(encoding="utf-8") as f: return list(csv.DictReader(f))

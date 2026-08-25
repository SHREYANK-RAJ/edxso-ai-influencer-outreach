import argparse
import csv
from app.models import Influencer
from app.pipeline import run_live, personalize_qualified, send_qualified

def load_seed(path="data/discovered_seed_50.csv"):
    items=[]
    with open(path,encoding="utf-8") as f:
        for r in csv.DictReader(f):
            er=r["engagement_rate"]
            items.append(Influencer(
                name=r["name"], platform=r["platform"], profile_url=r["profile_url"],
                followers=int(r["followers"]) if r["followers"] else None,
                engagement_rate=float(er.rstrip("%")) if er not in ("Not Available","") else None,
                category=r["niche"], content_themes=[r["content_theme"]],
                email=r["email"], geography=r["geography"], source=r["source"],
                source_url=r["source_url"]))
    return items

def main():
    p=argparse.ArgumentParser(description="Edxso AI Influencer Outreach")
    sub=p.add_subparsers(dest="cmd",required=True)
    d=sub.add_parser("discover"); d.add_argument("--limit",type=int,default=50)
    sub.add_parser("seed-demo")
    sub.add_parser("personalize")
    s=sub.add_parser("send"); s.add_argument("--real",action="store_true")
    args=p.parse_args()

    if args.cmd=="discover":
        items=personalize_qualified(run_live(args.limit))
        print(f"Processed {len(items)} live creators -> data/runtime_personalized.csv")
    elif args.cmd=="seed-demo":
        items=load_seed()
        items=personalize_qualified(items)
        print(f"Processed {len(items)} seed records -> data/runtime_personalized.csv")
    elif args.cmd=="personalize":
        print("Use seed-demo or discover first; personalization is integrated into those flows.")
    elif args.cmd=="send":
        items=load_seed()
        items=personalize_qualified(items)
        results=send_qualified(items,dry_run=not args.real)
        print(results)

if __name__=="__main__":
    main()

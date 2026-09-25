import argparse
from app.pipeline import run_live, run_seed, personalize_qualified, send_qualified

def main():
    p=argparse.ArgumentParser(description="Edxso AI Influencer Outreach")
    sub=p.add_subparsers(dest="cmd",required=True)
    d=sub.add_parser("discover"); d.add_argument("--limit",type=int,default=50)
    sub.add_parser("seed-demo")
    sub.add_parser("personalize")
    s=sub.add_parser("send"); s.add_argument("--real",action="store_true")
    args=p.parse_args()

    if args.cmd=="discover":
        items=personalize_qualified(run_live(limit=args.limit))
        print(f"Processed {len(items)} live creators -> data/runtime_personalized.csv")
    elif args.cmd=="seed-demo":
        items=run_seed()
        items=personalize_qualified(items)
        print(f"Processed {len(items)} seed records -> data/runtime_personalized.csv")
    elif args.cmd=="personalize":
        print("Use seed-demo or discover first; personalization is integrated into those flows.")
    elif args.cmd=="send":
        items=run_seed()
        items=personalize_qualified(items)
        results=send_qualified(items,dry_run=not args.real)
        print(results)

if __name__=="__main__":
    main()

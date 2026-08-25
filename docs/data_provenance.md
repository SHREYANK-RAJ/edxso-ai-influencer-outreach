# Data provenance

`data/discovered_seed_50.csv` is a research/demo seed assembled from public influencer
directory pages on 2026-08-25:

- Tring: https://www.tring.co.in/influencer-marketing/top-tech-micro-influencers-in-india
- Qoruz: https://qoruz.com/find-influencers/top-tech-micro-influencers-india
- Socialveins: https://socialveins.com/influencers/lists/top-tech-micro-influencers-india

The seed is deliberately transparent:
- `source` and `source_url` are stored per record.
- `captured_on` is stored.
- missing engagement/email is `Not Available` / `Not Found`.
- no email is synthetically generated.
- some records are outside the micro range so the filter can demonstrate explainable rejection.

For the final live demo, run the YouTube discovery adapter to satisfy the 50+ live discovery
test-run requirement rather than presenting the seed as live API output.

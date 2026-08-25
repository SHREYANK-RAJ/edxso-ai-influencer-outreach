# Edxso AI Engineer Intern — Assignment 1

## Automated Micro-Influencer Outreach System

**Workflow:** Discovery → Enrichment → Filtering → AI Personalization → Review → Sending/Simulation → Tracking.

### Chosen niche
Technology/gadgets in India.

### Stack
Python, YouTube Data API v3, FastAPI, Streamlit, Groq, Gmail API, SQLite, pytest.

### Live discovery
Set `YOUTUBE_API_KEY` in `.env`, then:

```bash
python -m app.cli discover --limit 50
```

For a credential-free local demo using the included public research seed:

```bash
python -m app.cli seed-demo
```

or use the Streamlit dashboard:

```bash
streamlit run app/dashboard.py
```

The working discovery adapter searches YouTube channels, retrieves subscriber statistics,
fetches recent videos, and calculates an engagement proxy from available views/likes/comments.
The API's subscriber statistics are rounded by YouTube, so the system treats them as estimates.

### Qualification
Default:
- 5,000–100,000 followers/subscribers
- technology relevance
- engagement >= 1% when available
- public contact email required

Every failure is stored as an explicit reason. Unknown data never becomes a pass.

### Email enrichment
Only public emails are accepted. Missing emails remain `Not Found`. No guessing.

### Personalization
Groq is optional. Without a key, a deterministic local fallback lets the pipeline be tested.
With Groq, the prompt requires a 60–90 word email and 15–30 word Instagram DM, using creator
signals such as niche, recent titles and content themes.

Creator text is explicitly treated as untrusted reference data to reduce prompt-injection risk.

### Sending
Gmail adapter uses OAuth and `gmail.send`. Dry-run is the default. SQLite prevents duplicate
outreach by unique email. Instagram DM is intentionally manual/simulated rather than bypassing
platform restrictions.

### Included seed dataset
`data/discovered_seed_50.csv` contains 50 public research records collected from public
influencer-directory pages on 2026-08-25. It is a reproducible research seed, not a claim of
live API freshness. Fields unavailable from the source are marked `Not Found`/`Not Available`.

### Tests
```bash
pytest -q
```

### Assignment mapping
- Discovery: `app/discovery/youtube.py`
- Filtering: `app/filtering.py`
- Enrichment: `app/discovery/youtube.py`
- AI personalization: `app/personalization/llm.py`
- Sending: `app/sending/`
- Tracking: `app/storage/db.py`
- UI: `app/dashboard.py`
- API: `app/api.py`
- Tests: `tests/`

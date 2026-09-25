# Architecture

Discovery adapters feed normalized `Influencer` objects into enrichment, explainable
filtering, personalization, and sending adapters. SQLite provides idempotent outreach
tracking. FastAPI exposes results; Streamlit provides the review UI.

Security: public data only, no guessed emails, no Instagram restriction bypass, dry-run
sending by default, secrets in environment variables, creator text treated as untrusted
LLM input.

Scale path: PostgreSQL + queue workers + provider rate-limiters + batch LLM calls.

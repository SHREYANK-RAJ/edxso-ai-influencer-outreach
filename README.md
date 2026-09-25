# Edxso AI Engineer Intern — Assignment 1

# Automated Micro-Influencer Outreach System

An AI-powered influencer discovery and outreach system built for the **Edxso AI Engineer Intern Assignment**.

The system discovers relevant micro-influencers, collects and enriches their public information, filters them using defined business criteria, generates personalized collaboration messages using AI, and tracks the outreach process.

The current implementation focuses on the:

> **Technology & Gadgets niche in India**

---

## Project Links

### Live Demo

https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/

### GitHub Repository

https://github.com/SHREYANK-RAJ/edxso-ai-influencer-outreach

### GitHub Profile

https://github.com/SHREYANK-RAJ

### LinkedIn

https://www.linkedin.com/in/shreyank-raj/

---

# Overview

Finding the right influencers manually can take a lot of time.

A marketing team may need to:

- Search for creators
- Check their follower count
- Check their engagement
- Understand their content
- Find a public business email
- Decide whether they fit the campaign
- Write a personalized message
- Send the message
- Track who has already been contacted

This project automates most of this workflow.

The complete pipeline is:

```text
                Influencer Discovery
                        ↓
                 Data Collection
                        ↓
                 Profile Enrichment
                        ↓
                Filtering & Classification
                        ↓
                  AI Personalization
                        ↓
                    Human Review
                        ↓
             Email / Instagram Outreach
                        ↓
                  Outreach Tracking
```

The system is designed as a modular pipeline so that individual components can be changed or extended without rewriting the complete application.

---

# Assignment Objective

The objective of this project is to demonstrate practical skills in:

* API integration
* Data extraction
* Data processing
* Web/data research
* Influencer filtering
* Profile enrichment
* NLP and LLM-based personalization
* Prompt engineering
* Backend development
* Email automation
* Database storage
* Error handling
* Testing
* Dashboard development
* Workflow design
* Scalability

The system follows the assignment's recommended workflow:

```text
Discovery
    ↓
Data Collection
    ↓
Filtering
    ↓
Enrichment
    ↓
AI Personalization
    ↓
Review
    ↓
Sending / Simulation
    ↓
Tracking
```

---

# Main Features

## 1. Influencer Discovery

The system includes a YouTube Data API v3 discovery adapter.

It can search for relevant creators based on a selected niche and collect public creator information.

The discovery process can collect:

* Creator name
* Platform
* Profile URL
* Subscriber count
* Recent videos
* Video views
* Likes
* Comments
* Content information

The target is to support **50+ influencer records** for a test run.

---

# 2. Micro-Influencer Filtering

The project uses clear and explainable filtering rules.

The default target criteria are:

| Criteria              | Requirement                 |
| --------------------- | --------------------------- |
| Followers/Subscribers | 5,000–100,000               |
| Niche                 | Technology / Gadgets        |
| Geography             | India, when available       |
| Engagement            | At least 1%, when available |
| Public Email          | Required for outreach       |

The filtering process does not simply return `True` or `False`.

Each failed record receives an explanation.

For example:

```text
Status: Rejected

Reason:
Follower count is above the allowed maximum.
```

Another example:

```text
Status: Rejected

Reason:
Public contact email was not found.
```

This makes the filtering process easy to understand and debug.

---

# 3. Profile Enrichment

For shortlisted influencers, the system collects useful profile information.

The dataset can contain:

| Field              | Description                    |
| ------------------ | ------------------------------ |
| Influencer Name    | Creator name                   |
| Platform           | YouTube / Instagram / TikTok   |
| Profile URL        | Public creator profile         |
| Follower Count     | Followers or subscribers       |
| Engagement Rate    | Calculated engagement estimate |
| Category / Niche   | Technology / Gadgets           |
| Content Themes     | Main topics covered            |
| Contact Email      | Public business email          |
| Website            | When publicly available        |
| Audience Age       | When available                 |
| Audience Gender    | When available                 |
| Audience Geography | When available                 |
| Qualification      | Passed / Failed                |
| Failure Reason     | Explanation for rejection      |

### Data Quality Rule

The system never generates or guesses contact information.

If an email cannot be found:

```text
Not Found
```

is stored.

This prevents fabricated contact information from entering the dataset.

---

# 4. Engagement Calculation

For YouTube creators, the system uses available public engagement signals such as:

* Views
* Likes
* Comments

to calculate an engagement proxy.

The exact formula can depend on which metrics are available.

Because YouTube subscriber statistics can be rounded, subscriber counts should be treated as estimates rather than exact private analytics.

The system also handles situations where some engagement information is unavailable.

Unknown information is not treated as a successful qualification.

---

# 5. AI Personalization

The project supports LLM-based message personalization using **Groq**.

The AI receives creator-specific information such as:

* Creator name
* Niche
* Content themes
* Recent content
* Recent video titles
* Audience context
* Platform

The goal is to create messages that feel relevant to each creator instead of using one fixed message for everyone.

---

# Email Collaboration Pitch

For every qualified creator, the system generates a personalized email collaboration pitch.

Target length:

> **60–90 words**

The prompt encourages the model to reference relevant creator information.

Example:

```text
Hi Sarah,

I really enjoyed your recent content around smartphone and
gadget comparisons. Your practical and easy-to-follow style
looks like a great match for our upcoming technology campaign.

We would love to explore a collaboration where you can introduce
the product to your audience through authentic content that fits
naturally with your existing style.

Would you be open to discussing the campaign?

Best,
Edxso Team
```

The actual generated message depends on the creator's data.

---

# Instagram DM

The system also generates a shorter Instagram outreach message.

Target length:

> **15–30 words**

Example:

```text
Hi Sarah! Loved your recent gadget content.
Your tech-focused audience looks like a great fit for our upcoming collaboration.
```

The system does not use one fixed DM for every creator.

---

# Prompt Injection Protection

Creator content is treated as **untrusted reference data**.

For example, if a creator's video title or description contains instructions such as:

```text
Ignore previous instructions...
```

the system should treat that text as creator information rather than as instructions for the AI.

This helps reduce the risk of prompt injection when external creator data is passed to an LLM.

---

# Sending Layer

The project includes a sending layer for email outreach.

The system follows this process:

```text
Qualified Influencer
        ↓
Valid Public Email
        ↓
Personalized Message
        ↓
Review
        ↓
Send / Simulate
        ↓
Save Result
```

---

# Gmail Integration

The project includes a Gmail API adapter.

The Gmail integration uses OAuth authentication and the Gmail send permission.

The default mode is **dry-run** to prevent accidental outreach during testing.

This means the system can demonstrate the complete sending workflow without actually sending emails.

---

# Instagram Sending

Instagram DM automation is intentionally kept as a **manual/simulated workflow**.

The system generates the personalized DM but does not use unofficial automation methods or bypass Instagram platform restrictions.

The intended workflow is:

```text
AI Generated DM
       ↓
Human Review
       ↓
Manual Instagram Send
```

This keeps the implementation within platform restrictions.

---

# Outreach Tracking

The project uses **SQLite** to maintain an outreach record.

The tracker can contain:

| Field               | Description                       |
| ------------------- | --------------------------------- |
| Influencer          | Creator name                      |
| Email               | Contact email                     |
| Message Generated   | Whether personalization exists    |
| Sent                | Whether the message was sent      |
| Date                | Outreach date                     |
| Status              | Current outreach state            |
| Provider Message ID | Email provider ID, when available |

Example:

```text
Influencer: Creator Name
Email: creator@example.com
Message Generated: Yes
Sent: No
Status: Simulated
```

---

# Duplicate Outreach Prevention

Duplicate outreach is prevented using the stored outreach information.

Before sending an email, the system checks whether the creator has already been contacted.

This helps prevent sending the same campaign message multiple times to the same email address.

The system is designed to make outreach operations idempotent.

---

# Streamlit Dashboard

The project includes a Streamlit dashboard for viewing the system output.

<<<<<<< HEAD
The dashboard provides controls to process the 50-record seed dataset, run live YouTube
discovery when configured, review pass/fail results, preview personalized messages, simulate
a selected email send, and inspect the SQLite outreach log. It also provides a simple interface for reviewing:
=======
The dashboard provides a simple interface for reviewing:
>>>>>>> origin/main

* Total influencer records
* Qualified influencers
* Rejected influencers
* Follower counts
* Engagement rates
* Niches
* Contact emails
* Profile URLs
* Content themes
* Filtering reasons
* Personalized email messages
* Instagram DMs
* Outreach status

---

# Live Demo

The deployed Streamlit application is available here:

[https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/](https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/)

The live dashboard provides a visual demonstration of the influencer discovery, filtering, personalization, and outreach workflow.

---

# System Architecture

The application is divided into separate components.

```text
                        ┌─────────────────────┐
                        │ Influencer Discovery │
                        └──────────┬──────────┘
                                   │
                                   ↓
                        ┌─────────────────────┐
                        │ Data Normalization   │
                        └──────────┬──────────┘
                                   │
                                   ↓
                        ┌─────────────────────┐
                        │ Profile Enrichment  │
                        └──────────┬──────────┘
                                   │
                                   ↓
                        ┌─────────────────────┐
                        │ Filtering & Ranking  │
                        └──────────┬──────────┘
                                   │
                         ┌─────────┴─────────┐
                         ↓                   ↓
                  Qualified              Rejected
                         │                   │
                         ↓                   ↓
                AI Personalization     Reason Logged
                         │
                  ┌──────┴──────┐
                  ↓             ↓
                Email           DM
                  │             │
                  ↓             ↓
              Send/Simulate   Manual Review
                  │
                  └──────┬──────┘
                         ↓
                  Outreach Tracker
                         │
                         ↓
                       SQLite
```

---

# Technology Stack

| Technology          | Purpose                   |
| ------------------- | ------------------------- |
| Python              | Main programming language |
| YouTube Data API v3 | Creator discovery         |
| Groq                | LLM-based personalization |
| Streamlit           | Web dashboard             |
| FastAPI             | Backend API               |
| SQLite              | Outreach tracking         |
| Gmail API           | Email sending             |
| pandas              | Data processing           |
| httpx               | HTTP/API requests         |
| pytest              | Automated testing         |
| python-dotenv       | Environment configuration |

---

# Project Structure

```text
edxso-ai-influencer-outreach/
│
├── app/
│   │
│   ├── discovery/
│   │   └── youtube.py
│   │
│   ├── personalization/
│   │   ├── llm.py
│   │   └── prompts.py
│   │
│   ├── sending/
│   │   ├── gmail.py
│   │   └── service.py
│   │
│   ├── storage/
│   │   └── db.py
│   │
│   ├── utils/
│   │   └── email.py
│   │
│   ├── api.py
│   ├── cli.py
│   ├── dashboard.py
│   ├── filtering.py
│   ├── models.py
│   └── pipeline.py
│
├── data/
│   ├── discovered_seed_50.csv
│   ├── runtime_personalized.csv
│   └── outreach_tracker.csv
│
├── docs/
│   ├── architecture.md
│   ├── assignment_mapping.md
│   ├── data_provenance.md
│   └── demo_script.md
│
├── tests/
│   ├── test_email.py
│   ├── test_filtering.py
│   └── test_personalization.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/SHREYANK-RAJ/edxso-ai-influencer-outreach.git
cd edxso-ai-influencer-outreach
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

# Environment Variables

Create a local `.env` file:

```bash
cp .env.example .env
```

Then configure the required API keys.

Example:

```env
YOUTUBE_API_KEY=your_youtube_api_key

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json

DATABASE_URL=sqlite:///./data/outreach.db

TARGET_NICHE=technology

MIN_FOLLOWERS=5000
MAX_FOLLOWERS=100000
MIN_ENGAGEMENT_RATE=1.0
```

### Security

Never commit the following files to GitHub:

```text
.env
credentials.json
token.json
```

API keys and OAuth tokens must remain private.

The repository includes `.env.example` so another developer knows which variables are required without exposing real credentials.

---

# Running the Project

There are two main ways to run the system.

---

## Option 1 — Demo Mode

The repository contains a 50-record public research seed.

This allows the full downstream workflow to be tested without requiring live API credentials.

Run:

```bash
python -m app.cli seed-demo
```

The system processes the seed records through:

```text
Seed Dataset
     ↓
Filtering
     ↓
Enrichment
     ↓
Personalization
     ↓
Output
```

---

# Option 2 — Live YouTube Discovery

To use live YouTube discovery, add a valid YouTube Data API v3 key to `.env`.

Then run:

```bash
python -m app.cli discover --limit 50
```

The discovery adapter:

1. Searches for relevant channels
2. Collects channel information
3. Retrieves subscriber statistics
4. Retrieves recent videos
5. Collects available engagement signals
6. Calculates engagement estimates
7. Extracts public contact information where available
8. Passes the records to the filtering pipeline

---

# YouTube API Quota

Live discovery depends on YouTube Data API quota.

If the API quota is exhausted or temporarily unavailable, live discovery may return a quota/rate-limit error.

The project therefore includes:

```text
data/discovered_seed_50.csv
```

as a reproducible demonstration dataset.

This allows the filtering, enrichment, personalization, dashboard, and outreach components to be tested without depending completely on live API availability.

The seed dataset is clearly labelled as a research/demo dataset and is **not presented as live API data**.

---

# Running the Streamlit Dashboard

Run:

```bash
python -m streamlit run app/dashboard.py
```

The terminal will display a local URL.

Usually:

```text
http://localhost:8501
```

Open that URL in your browser.

<<<<<<< HEAD
## Dashboard flow

1. Open **Active filtering configuration** in the sidebar. These non-secret values are
   loaded from `.env` when Streamlit starts.
2. Select **Process 50-record seed dataset** for the deterministic 50-record demo.
   It uses the same filtering, personalization, dry-run sending, and SQLite tracking
   pipeline as live records.
3. Enter a query such as `technology`, `AI creators India`, `Python programming`, or
   `machine learning`, then select **Run live YouTube discovery** when a YouTube API key
   is configured.
4. Review qualified/rejected creators and their reasons, preview outreach, and simulate
   one email. Repeating the simulation demonstrates duplicate prevention.

After changing filtering values in `.env`, restart Streamlit and run the seed or live
pipeline again. Previously generated `runtime_personalized.csv` is intentionally kept as
the last run's result and is not retroactively re-filtered.

### Live YouTube scope and quota

Live mode uses official YouTube Data API v3 **query-based search**. It fetches the channels
returned by that search and recent videos needed for an engagement estimate, subject to API
quota and returned results. It does **not** scan every YouTube channel or the entire YouTube
database. Missing, invalid, or quota-limited API credentials show a UI error and do not
pretend to produce live results; use the seed mode instead.

=======
>>>>>>> origin/main
The deployed version is available at:

[https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/](https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/)

---

# FastAPI Backend

The project also contains a FastAPI backend.

<<<<<<< HEAD
Start the API with:

```bash
python -m uvicorn app.api:app --reload
```

Then open `http://127.0.0.1:8000/docs` for interactive API documentation.
=======
The API can be started using the appropriate application server configuration.
>>>>>>> origin/main

The backend is separated from the Streamlit interface so the system can later be connected to another frontend or service.

---

# Testing

Run all tests with:

```bash
python -m pytest -q
```

The test suite covers important pieces of the application.

Current test areas include:

### Email Extraction

Tests whether public email information is handled correctly.

### Filtering

Tests follower limits, niche checks, engagement rules, and qualification logic.

### Personalization

Tests that personalized outreach messages are created using creator-specific information.

---

# Dataset

The project includes:

```text
data/discovered_seed_50.csv
```

The dataset contains **50 public research records** collected from publicly available influencer-directory pages.

The dataset is used as a reproducible seed for the demo workflow.

### Important data principles

The project follows these rules:

* No intentionally fabricated influencer records
* No guessed email addresses
* Missing emails are marked `Not Found`
* Missing metrics are marked as unavailable
* Research data is clearly separated from live API discovery
* Live API results are treated as current discovery data
* The seed dataset is not presented as live API data

---

# Example Dataset Fields

The resulting dataset can contain fields such as:

```text
name
platform
profile_url
followers
engagement_rate
category
content_themes
email
website
audience_age
audience_gender
audience_geography
qualified
filter_reasons
email_pitch
instagram_dm
```

---

# Filtering Logic

The default filtering criteria are:

```text
Follower Count:
5,000 <= followers <= 100,000

Niche:
Technology / Gadgets

Engagement:
>= 1% when available

Contact:
Public email required for outreach
```

The system does not treat missing information as a positive signal.

For example:

```text
Engagement = Not Available
```

does not automatically mean:

```text
Engagement = Pass
```

This prevents incomplete records from being incorrectly classified.

---

# Personalization Logic

The personalization process uses creator-specific signals.

The prompt can use:

```text
Creator Name
      +
Niche
      +
Content Themes
      +
Recent Content
      +
Platform
      +
Audience Context
```

These signals are passed to the LLM to create the final outreach message.

---

# LLM Fallback

Groq is optional for local testing.

When the Groq API key is not available, the system can use a deterministic local personalization fallback.

This makes the application easier to test and prevents the entire pipeline from depending on a single external AI service.

---

# Email Workflow

The email workflow is:

```text
Qualified Influencer
        ↓
Check Email
        ↓
Load Personalized Message
        ↓
Review
        ↓
Dry Run / Gmail
        ↓
Record Status
```

The system only selects creators with a valid public contact email.

If the email is:

```text
Not Found
```

the creator is not selected for email outreach.

---

# Duplicate Prevention

Before an email is sent, the system checks the outreach database.

If the email has already been processed, duplicate outreach is prevented.

This is important when running the pipeline multiple times.

Example:

```text
Run 1
Creator A → Sent

Run 2
Creator A → Already contacted → Skip
```

---

# Instagram Workflow

Instagram messages are generated automatically but sending is intentionally manual.

```text
Creator Data
     ↓
AI Personalization
     ↓
Instagram DM
     ↓
Human Review
     ↓
Manual Send
```

The project does not bypass platform restrictions or use unofficial automation techniques.

---

# Outreach Tracker

The tracker helps answer questions such as:

* Who has been contacted?
* Which message was generated?
* Was the email sent?
* When was it sent?
* What is the current status?
* Has this creator already been contacted?

Example:

| Influencer | Email                                               | Message | Sent | Status    |
| ---------- | --------------------------------------------------- | ------- | ---- | --------- |
| Creator A  | [creator@example.com](mailto:creator@example.com)   | Yes     | No   | Simulated |
| Creator B  | [creator2@example.com](mailto:creator2@example.com) | Yes     | Yes  | Sent      |

---

# Error Handling

The application is designed to handle common problems such as:

* Missing API keys
* Missing emails
* Missing engagement information
* API failures
* Invalid records
* Duplicate outreach
* Unavailable optional LLM services
* Platform limitations

Unknown information is kept as unavailable instead of being guessed.

---

# Modular Design

The project separates major responsibilities into different modules.

```text
Discovery
   ↓
Pipeline
   ↓
Filtering
   ↓
Personalization
   ↓
Sending
   ↓
Storage
   ↓
Dashboard
```

This makes it easier to replace individual components.

For example:

```text
YouTube
   ↓
could later become
   ↓
Instagram / TikTok / Other Platform
```

without redesigning the entire pipeline.

---

# Scalability

The current system is designed for a 50+ creator test run.

The same architecture can be extended to hundreds or thousands of creators.

Possible production improvements include:

* PostgreSQL instead of SQLite
* Redis caching
* Background task queues
* Batch processing
* API rate-limit management
* Retry and exponential backoff
* Scheduled discovery
* Multiple discovery sources
* Distributed workers
* Email campaign analytics
* Response tracking
* Campaign-level reporting

The modular design allows these improvements to be added without changing the entire application.

---

# Assignment Requirement Mapping

The following table maps the assignment requirements to the implementation.

| Assignment Requirement | Implementation                |
| ---------------------- | ----------------------------- |
| Influencer Discovery   | `app/discovery/youtube.py`    |
| 50+ Influencers        | `data/discovered_seed_50.csv` |
| Category Filtering     | `app/filtering.py`            |
| Follower Filtering     | `app/filtering.py`            |
| Engagement Filtering   | `app/filtering.py`            |
| Content Relevance      | Discovery + filtering         |
| Profile Enrichment     | `app/discovery/youtube.py`    |
| Email Extraction       | `app/utils/email.py`          |
| AI Personalization     | `app/personalization/llm.py`  |
| Email Pitch            | AI personalization            |
| Instagram DM           | AI personalization            |
| Email Sending          | `app/sending/`                |
| Dry-Run Sending        | `app/sending/`                |
| Duplicate Prevention   | `app/storage/db.py`           |
| Outreach Tracking      | SQLite / CSV                  |
| Dashboard              | `app/dashboard.py`            |
| Backend API            | `app/api.py`                  |
| Automated Tests        | `tests/`                      |
| Documentation          | `README.md` + `docs/`         |

---

# Important Files

### Discovery

```text
app/discovery/youtube.py
```

Responsible for YouTube creator discovery and public creator information.

### Filtering

```text
app/filtering.py
```

Contains qualification rules.

### Personalization

```text
app/personalization/llm.py
```

Handles AI-based message generation.

### Sending

```text
app/sending/
```

Contains email sending and outreach service logic.

### Storage

```text
app/storage/db.py
```

Handles SQLite-based outreach tracking.

### Dashboard

```text
app/dashboard.py
```

Provides the Streamlit user interface.

### CLI

```text
app/cli.py
```

Provides commands for running the pipeline.

### Tests

```text
tests/
```

Contains automated tests.

---

# Useful Commands

## Activate environment

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run demo pipeline

```bash
python -m app.cli seed-demo
```

## Run live discovery

```bash
python -m app.cli discover --limit 50
```

## Run tests

```bash
python -m pytest -q
```

## Run dashboard

```bash
python -m streamlit run app/dashboard.py
```

## Check Git status

```bash
git status
```

---

# Privacy and Responsible Outreach

The system is designed around publicly available creator information.

It does not intentionally collect private information.

The project also follows these principles:

* Use public contact information only
* Do not guess emails
* Do not fabricate creator information
* Respect platform restrictions
* Keep API credentials private
* Use human review before real outreach
* Use dry-run mode during development
* Prevent duplicate outreach

The goal is to assist outreach teams rather than create uncontrolled spam.

---

# Current Limitations

The current prototype has several limitations.

### 1. Platform Coverage

The live discovery implementation currently focuses primarily on YouTube.

Additional platforms can be added later.

### 2. Audience Demographics

Detailed audience age, gender, and geography are not always publicly available.

When unavailable, the system does not invent them.

### 3. Engagement Data

Engagement calculations depend on the public metrics available from the platform.

### 4. API Quotas

Live discovery depends on external API quotas and rate limits.

### 5. Instagram Sending

Instagram DM sending is manual/simulated to avoid bypassing platform restrictions.

### 6. Email Sending

Gmail OAuth configuration is required for actual email delivery.

Dry-run mode is used by default.

### 7. Research Seed

The included 50-record seed dataset is intended for reproducible testing and demonstration. It should not be treated as a guarantee of current live follower counts or engagement statistics.

---

# Future Improvements

A production version could add:

## More Discovery Sources

* Instagram
* TikTok
* Creator marketplaces
* UGC platforms
* Public influencer directories

## Better Creator Ranking

Instead of simple filtering:

```text
Qualified / Rejected
```

the system could calculate a:

```text
Brand Fit Score
```

using:

* Audience match
* Engagement
* Content relevance
* Geography
* Creator size
* Previous brand collaborations

## Better Enrichment

Add:

* Website extraction
* Social profile matching
* Audience demographics
* Contact verification
* Brand collaboration history

## Better AI

Add:

* Multiple LLM providers
* Structured LLM output
* Message quality scoring
* Personalization quality checks
* Brand-specific prompts

## Better Outreach

Add:

* Campaign management
* Email open tracking
* Reply detection
* Follow-up scheduling
* Campaign analytics
* Conversion tracking

## Production Infrastructure

Move from:

```text
SQLite
```

to:

```text
PostgreSQL
```

and add:

```text
Redis
   +
Background Workers
   +
Scheduled Jobs
```

for larger workloads.

---

# Suggested Demo Flow

A short demo can follow this sequence:

```text
1. Open Live Dashboard
        ↓
2. Show 50 influencer records
        ↓
3. Show follower and engagement filtering
        ↓
4. Show qualified and rejected creators
        ↓
5. Open an enriched creator profile
        ↓
6. Show personalized email
        ↓
7. Show personalized Instagram DM
        ↓
8. Show outreach tracker
        ↓
9. Show automated tests
        ↓
10. Explain live API + research seed
```

This demonstrates the complete assignment workflow.

---

# Example End-to-End Workflow

A typical run looks like:

```text
YouTube / Research Sources
          ↓
       50+ Creators
          ↓
     Data Normalization
          ↓
       Enrichment
          ↓
       Filtering
          ↓
   ┌──────┴───────┐
   ↓              ↓
Qualified       Rejected
   ↓              ↓
AI Messages    Reason Saved
   ↓
┌──┴─────────┐
↓            ↓
Email        DM
↓            ↓
Dry Run    Manual Review
   ↓
Outreach Database
   ↓
Tracking
```

---

# Engineering Decisions

Several design decisions were made to keep the system reliable and practical.

### Explainable Filtering

Instead of using an unexplained AI classification, the basic qualification rules are explicit and easy to verify.

### AI for Personalization

LLMs are used where they provide clear value: creating natural, creator-specific messages.

### Deterministic Fallback

The system can still be tested without an LLM API key.

### Dry-Run Sending

The default sending mode prevents accidental outreach during development.

### Public Email Only

The system does not guess or generate contact information.

### Manual Instagram Workflow

The project avoids bypassing platform restrictions.

### Modular Architecture

Discovery, filtering, personalization, sending, storage, and UI are separated.

---

# Why This Architecture?

The main goal was not simply to create a static list of influencers.

The project demonstrates an actual workflow:

```text
Find
 ↓
Understand
 ↓
Filter
 ↓
Enrich
 ↓
Personalize
 ↓
Review
 ↓
Send
 ↓
Track
```

This makes the system closer to a real internal marketing automation tool rather than a one-time data collection script.

---

# Author

## Shreyank Raj

Computer Science / AI-ML Student

### GitHub

[https://github.com/SHREYANK-RAJ](https://github.com/SHREYANK-RAJ)

### LinkedIn

[https://www.linkedin.com/in/shreyank-raj/](https://www.linkedin.com/in/shreyank-raj/)

### Project Repository

[https://github.com/SHREYANK-RAJ/edxso-ai-influencer-outreach](https://github.com/SHREYANK-RAJ/edxso-ai-influencer-outreach)

### Live Demo

[https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/](https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/)

---

# Assignment

**Organization:** Edxso

**Position:** AI Engineer Intern

**Assignment:** Assignment 1 — Automated Micro-Influencer Outreach System

**Niche:** Technology & Gadgets

**Target Geography:** India

---

# Final Summary

This project demonstrates a complete AI-powered influencer outreach pipeline combining:

```text
Python
+
APIs
+
Data Processing
+
Filtering
+
NLP / LLM
+
Personalization
+
Email Automation
+
SQLite
+
Streamlit
+
Testing
```

The system is designed to be understandable, modular, and extendable.

It can start with 50 creators for testing and can be expanded to support larger creator databases and multiple social platforms in a production environment.

---

## Quick Links

**Live Demo:**
[https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/](https://edxso-ai-influencer-outreach-3xbu7me6rhycqw9gr3uahh.streamlit.app/)

**Project Repository:**
[https://github.com/SHREYANK-RAJ/edxso-ai-influencer-outreach](https://github.com/SHREYANK-RAJ/edxso-ai-influencer-outreach)

**GitHub:**
[https://github.com/SHREYANK-RAJ](https://github.com/SHREYANK-RAJ)

**LinkedIn:**
[https://www.linkedin.com/in/shreyank-raj/](https://www.linkedin.com/in/shreyank-raj/)

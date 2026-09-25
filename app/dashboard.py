from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st

from app.config import settings
from app.models import Influencer
from app.pipeline import personalize_qualified, run_live, run_seed
from app.sending.service import OutreachService
from app.storage.db import OutreachDB

DATA_DIR = ROOT_DIR / "data"
PERSONALIZED_PATH = DATA_DIR / "runtime_personalized.csv"


def load_display_data():
    path = PERSONALIZED_PATH if PERSONALIZED_PATH.exists() else DATA_DIR / "discovered_seed_50.csv"
    return pd.read_csv(path), path


def row_to_influencer(row):
    def number(value):
        return None if pd.isna(value) else float(value)

    followers = number(row.get("followers"))
    engagement = number(row.get("engagement_rate"))
    return Influencer(
        name=str(row.get("name", "Unknown")), platform=str(row.get("platform", "Unknown")),
        profile_url=str(row.get("profile_url", "")),
        followers=int(followers) if followers is not None else None,
        engagement_rate=engagement, category=str(row.get("category", row.get("niche", "technology"))),
        content_themes=str(row.get("content_themes", row.get("content_theme", ""))).split("; "),
        email=str(row.get("email", "Not Found")), geography=str(row.get("geography", "Not Found")),
        email_pitch=str(row.get("email_pitch", "")), instagram_dm=str(row.get("instagram_dm", "")),
        qualified=str(row.get("qualified", "False")).lower() == "true",
    )


st.set_page_config(page_title="Edxso Influencer Outreach", layout="wide")
st.title("Edxso — AI Micro-Influencer Outreach")
st.caption("Public-data only • email sending defaults to dry-run")

with st.sidebar:
    st.header("Pipeline controls")
    with st.expander("Active filtering configuration", expanded=True):
        st.write(f"**Target niche:** {settings.target_niche}")
        st.write(f"**Follower range:** {settings.min_followers:,}–{settings.max_followers:,}")
        st.write(f"**Minimum engagement:** {settings.min_engagement_rate}%")
        st.caption("Values are loaded from .env at startup. Restart Streamlit after editing .env, then run a fresh pipeline.")
    st.caption("The seed dataset is a transparent 50-record research/demo source.")
    if st.button("Process 50-record seed dataset", width="stretch"):
        with st.spinner("Filtering and generating personalized outreach..."):
            items = personalize_qualified(run_seed())
        st.success(f"Processed {len(items)} seed records; {sum(i.qualified for i in items)} qualified.")
    st.divider()
    query = st.text_input("YouTube search query", value=settings.target_niche,
                          help="Examples: technology, AI creators India, Python programming, machine learning.")
    target = st.number_input("Live discovery target", min_value=50, max_value=100, value=50,
                             help="50 is enough for the assignment; larger runs use more YouTube API quota.")
    if st.button("Run live YouTube discovery", width="stretch"):
        try:
            with st.spinner("Discovering, enriching, filtering, and personalizing..."):
                items = personalize_qualified(run_live(query=query, limit=int(target)))
            st.success(f"Processed {len(items)} live creators; {sum(i.qualified for i in items)} qualified.")
        except Exception as exc:
            st.error(f"Live discovery could not run: {exc}")
            st.info("No live data was fabricated. Process the seed dataset to continue the deterministic demo.")

df, source_path = load_display_data()
is_processed = "qualified" in df.columns
if not is_processed:
    st.info("Showing the 50-record seed dataset. Select “Process 50-record seed dataset” to run filtering and generate messages locally.")

overview_tab, messages_tab, outreach_tab = st.tabs(["Dataset & filtering", "Personalized messages", "Outreach tracker"])

with overview_tab:
    display_df = df.copy()
    st.caption(f"Data source: `{source_path.name}`")
    left, middle, right = st.columns(3)
    left.metric("Records", len(df))
    if is_processed:
        qualified = display_df["qualified"].astype(str).str.lower().eq("true")
        middle.metric("Qualified", int(qualified.sum()))
        right.metric("Rejected", int((~qualified).sum()))
        choice = st.radio("View", ["All records", "Qualified", "Rejected"], horizontal=True)
        if choice == "Qualified":
            display_df = display_df[qualified]
        elif choice == "Rejected":
            display_df = display_df[~qualified]
    st.dataframe(display_df, width="stretch", hide_index=True)
    st.download_button("Download current dataset CSV", display_df.to_csv(index=False).encode("utf-8"), "influencer_results.csv", "text/csv")

with messages_tab:
    if not is_processed or "email_pitch" not in df.columns:
        st.info("Process the seed dataset or complete a live discovery run to generate messages.")
    else:
        qualified_rows = df[df["qualified"].astype(str).str.lower().eq("true")]
        if qualified_rows.empty:
            st.warning("No creators qualify under the current filter criteria.")
        else:
            selected_name = st.selectbox("Qualified creator", qualified_rows["name"].tolist())
            record = qualified_rows[qualified_rows["name"] == selected_name].iloc[0]
            st.subheader("Email collaboration pitch")
            st.write(record.get("email_pitch", "No message was generated."))
            mode = str(record.get("personalization_mode", "not_generated"))
            if mode.startswith("fallback"):
                st.info("Fallback personalization was used because Groq is not configured or was unavailable.")
            elif mode == "groq":
                st.success("Generated with Groq personalization.")
            st.subheader("Instagram DM — manual review/send")
            st.write(record.get("instagram_dm", "No message was generated."))
            st.caption("Instagram delivery is intentionally manual; this app does not bypass platform restrictions.")

with outreach_tab:
    if not is_processed or "email_pitch" not in df.columns:
        st.info("Generate personalized messages before sending outreach.")
    else:
        candidates = df[(df["qualified"].astype(str).str.lower().eq("true")) & (df["email"].ne("Not Found"))]
        candidates = candidates.drop_duplicates(subset=["email"])
        if candidates.empty:
            st.warning("There are no qualified creators with a public email.")
        else:
            labels = {f"{row['name']} — {row['email']}": idx for idx, row in candidates.iterrows()}
            selected = st.selectbox("Email recipient", list(labels))
            row = candidates.loc[labels[selected]]
            st.caption("Dry-run records the simulated delivery in SQLite; it does not send an email.")
            if st.button("Simulate email send", type="primary"):
                result = OutreachService(OutreachDB()).send_email(row_to_influencer(row), dry_run=True)
                if result["status"] == "simulated":
                    st.success(f"Simulated and recorded: {result['message_id']}")
                else:
                    st.warning(result["reason"])
            st.caption("Real Gmail sending is available from the CLI only after OAuth credentials are configured.")

    records = OutreachDB().records()
    st.subheader("SQLite outreach log")
    if records:
        st.dataframe(pd.DataFrame(records), width="stretch", hide_index=True)
    else:
        st.caption("No outreach has been recorded yet.")

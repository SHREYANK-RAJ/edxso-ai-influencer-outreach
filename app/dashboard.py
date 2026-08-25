from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import streamlit as st
import pandas as pd
from pathlib import Path
from app.pipeline import run_live, personalize_qualified

st.set_page_config(page_title="Edxso Influencer Outreach",layout="wide")
st.title("Edxso — AI Micro-Influencer Outreach")
st.caption("Technology niche • public-data only • dry-run sending by default")

target=st.sidebar.number_input("Discovery target",50,500,50)
if st.sidebar.button("Run live discovery"):
    with st.spinner("Discovering, enriching and filtering..."):
        items=personalize_qualified(run_live(int(target)))
    st.success(f"Processed {len(items)} creators.")

p=Path("data/runtime_personalized.csv")
if not p.exists(): p=Path("data/discovered_seed_50.csv")
if p.exists():
    df=pd.read_csv(p)
    st.metric("Records",len(df))
    if "qualified" in df.columns:
        st.metric("Qualified",int(df["qualified"].astype(str).str.lower().eq("true").sum()))
    st.dataframe(df,use_container_width=True)
    if "email_pitch" in df.columns:
        st.subheader("Personalized outreach preview")
        for _,r in df.head(10).iterrows():
            with st.expander(str(r.get("name","Creator"))):
                st.write("Email:",r.get("email_pitch",""))
                st.write("Instagram DM:",r.get("instagram_dm",""))

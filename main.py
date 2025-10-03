import streamlit as st
import pandas as pd
import re
from datetime import datetime

st.set_page_config(page_title="Caprae Lead Tool — Shreerama D S", layout="wide")

# Helper functions
def validate_email(email: str) -> bool:
    if not isinstance(email, str) or email.strip() == "":
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email.strip()))

FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "live.com", "icloud.com",
    "aol.com", "mail.com", "protonmail.com"
}

def enrich_lead(company: str, email: str):
    domain = "unknown"
    provider_free = False
    if isinstance(email, str) and "@" in email:
        domain = email.split("@")[-1].lower().strip()
        if domain in FREE_EMAIL_DOMAINS:
            provider_free = True
    comp_slug = "".join(c if c.isalnum() or c == "-" else "-" for c in company.lower().replace(" ", "-"))
    linkedin_url = f"https://www.linkedin.com/company/{comp_slug}"
    return domain, linkedin_url, provider_free

def score_lead(industry: str, email_valid: bool, company: str, is_free_email: bool) -> int:
    score = 40 if email_valid else 10
    high_value_keywords = ["artificial", "ai", "machine learning", "fintech", "edtech", "saas", "analytics", "data"]
    industry_text = (industry or "").lower()
    for kw in high_value_keywords:
        if kw in industry_text:
            score += 20
            break
    else:
        score += 5
    company_text = (company or "").lower()
    for kw in ["ai", "ml", "data", "cloud", "analytics"]:
        if kw in company_text:
            score += 10
            break
    if is_free_email:
        score -= 10
    score = max(0, min(100, score))
    return int(score)

def priority_label(score: int) -> str:
    if score >= 75:
        return "High 🔥"
    if score >= 50:
        return "Medium 🔷"
    return "Low ⚪"

def deduplicate(df: pd.DataFrame) -> pd.DataFrame:
    if "Email" in df.columns:
        df = df.sort_values(by="Lead Score", ascending=False)
        df = df.drop_duplicates(subset=["Email"], keep="first")
    df = df.drop_duplicates(subset=["Company"], keep="first")
    return df.reset_index(drop=True)

def generate_report(df: pd.DataFrame) -> str:
    total = len(df)
    valid = int(df["Email Valid"].sum()) if "Email Valid" in df.columns else 0
    avg_score = round(df["Lead Score"].mean(), 2) if len(df) else 0
    high = int((df["Lead Score"] >= 75).sum()) if "Lead Score" in df.columns else 0
    medium = int(((df["Lead Score"] >= 50) & (df["Lead Score"] < 75)).sum()) if "Lead Score" in df.columns else 0
    low = total - high - medium
    lines = [
        f"Caprae Lead Tool — Report (generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})",
        f"Total leads processed: {total}",
        f"Valid emails: {valid}",
        f"Average lead score: {avg_score}",
        f"High priority (>=75): {high}",
        f"Medium priority (50-74): {medium}",
        f"Low priority (<50): {low}",
        "",
        "Top 5 leads (by score):"
    ]
    top5 = df.sort_values(by="Lead Score", ascending=False).head(5)
    for idx, row in top5.iterrows():
        lines.append(f"- {row['Company']} | {row.get('Email','')} | Score: {row['Lead Score']} | {row['LinkedIn']}")
    return "\n".join(lines)

def highlight_score(val):
    if val >= 75:
        return 'color: green; font-weight: bold;'
    elif val >= 50:
        return 'color: orange; font-weight: bold;'
    else:
        return 'color: red; font-weight: bold;'


# Sample data
SAMPLE_LEADS = [
    {"Company": "TechNova AI", "Industry": "Artificial Intelligence", "Email": "contact@technovaai.com"},
    {"Company": "GreenFarm Ltd", "Industry": "Agriculture", "Email": "info@greenfarm.com"},
    {"Company": "BuildMax", "Industry": "Construction", "Email": "sales.buildmax@gmail.com"},
    {"Company": "FinSolve", "Industry": "FinTech", "Email": "support@finsolve.io"},
    {"Company": "EduSmart", "Industry": "EdTech", "Email": "hello@edusmart.org"},
    {"Company": "DataWave", "Industry": "Analytics", "Email": "random_email@"}
]

# UI
st.title("Caprae Lead Tool — Shreerama D S")
st.markdown(
    """
    **What this tool does (demo):**  
    - Validate emails, enrich leads (domain + LinkedIn guess), deduplicate, score and prioritize leads.  
    - Export cleaned CSV and a short summary report — ready for CRM import.  
    """
)

with st.expander("How to use"):
    st.write("1. Upload a CSV with columns: `Company`, `Email`, `Industry` (optional). Or use the sample data.  2. Click `Process Leads`.  3. Review, download CSV and download short report.")

col1, col2 = st.columns([3,1])
with col1:
    uploaded_file = st.file_uploader("Upload leads CSV (Company, Email, Industry)", type=["csv"])
    use_sample = st.button("Use sample data")
with col2:
    st.write("Options")
    dedupe_toggle = st.checkbox("Deduplicate (recommended)", value=True)
    show_raw = st.checkbox("Show raw input after upload", value=False)

# Data persistence using session_state
if "df_input" not in st.session_state:
    st.session_state.df_input = None

if uploaded_file:
    try:
        st.session_state.df_input = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Failed to read CSV: {e}")

if use_sample:
    st.session_state.df_input = pd.DataFrame(SAMPLE_LEADS)

df_input = st.session_state.df_input


# Process
if df_input is None:
    st.info("Upload a CSV or click 'Use sample data' to get started.")
else:
    expected_cols = {"company", "email", "industry"}
    existing_cols = {c.lower(): c for c in df_input.columns}
    for target in expected_cols:
        if target in existing_cols:
            df_input = df_input.rename(columns={existing_cols[target]: target.capitalize()})
    for c in ["Company", "Email", "Industry"]:
        if c not in df_input.columns:
            df_input[c] = ""

    if show_raw:
        st.subheader("Raw input")
        st.dataframe(df_input.head(20))

    if st.button("Process Leads"):
        if df_input.empty:
            st.warning("No leads found in uploaded file.")
        else:
            df = df_input[["Company", "Email", "Industry"]].copy().fillna("")
            df["Email Valid"] = df["Email"].apply(validate_email)
            enriched = df.apply(lambda r: enrich_lead(r["Company"], r["Email"]), axis=1)
            df["Domain"] = enriched.apply(lambda x: x[0])
            df["LinkedIn"] = enriched.apply(lambda x: x[1])
            df["Is Free Email"] = enriched.apply(lambda x: x[2])
            df["Lead Score"] = df.apply(lambda r: score_lead(r["Industry"], r["Email Valid"], r["Company"], r["Is Free Email"]), axis=1)
            df["Priority"] = df["Lead Score"].apply(priority_label)

            df = df.sort_values(by="Lead Score", ascending=False).reset_index(drop=True)
            if dedupe_toggle:
                df = deduplicate(df)

            # Summary
            st.subheader("Summary")
            total = len(df)
            valid_count = int(df["Email Valid"].sum())
            avg_score = round(df["Lead Score"].mean(), 2) if total else 0
            c1, c2, c3 = st.columns(3)
            c1.metric("Total leads", total)
            c2.metric("Valid emails", valid_count)
            c3.metric("Average score", avg_score)

            st.subheader("Leads (sorted by score)")
            st.dataframe(df.style.applymap(highlight_score, subset=["Lead Score"]).format({"Lead Score": "{:.0f}"}).hide(axis="index"), height=420)

            csv_bytes = df.to_csv(index=False).encode("utf-8")
            ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
            st.download_button("Download cleaned leads (CSV)", data=csv_bytes, file_name=f"caprae_leads_{ts}.csv", mime="text/csv")

            report_text = generate_report(df)
            st.download_button("Download short report (txt)", data=report_text, file_name=f"caprae_report_{ts}.txt", mime="text/plain")

            st.subheader("Top 5 leads")
            st.table(df.head(5)[["Company", "Email", "Industry", "Lead Score", "Priority", "LinkedIn"]])

            st.success("Processing complete — export the CSV and the report to include in your submission.")
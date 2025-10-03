# Caprae Lead Tool — Shreerama D S
**Developer Intern — Caprae Capital (Handbook Submission)**

## What this project is
A focused 5-hour demo tool that demonstrates lead validation, enrichment, scoring and prioritization for B2B prospecting. The tool is a small, production-minded pipeline (Streamlit UI) that:
- Validates emails to reduce wasted outreach
- Enriches records with company domain and a guessed LinkedIn company URL
- Deduplicates leads
- Scores leads (0–100) and assigns priority labels (High/Medium/Low)
- Exports cleaned CSV and a short text report ready for CRM import

Code is intentionally compact, easy to run, and demonstrates business-first thinking: improving lead quality and sales efficiency.

## Files
- `main.py` — Streamlit app (UI + processing)
- `requirements.txt` — minimal dependencies
- `sample_output.csv` — sample CSV (generated when running app)
- `README.md` — this file
- `Report` — Sample Report (generated when running app)
- `Test_Dataset` — Sample Test Dataset

## How to run
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate      # Windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run main.py
   ```
# Caprae Lead Tool — Shreerama D S  
**Developer Intern — Caprae Capital (Handbook Submission)**  

🔗 **Live Demo:** [caprae-lead-tool.streamlit.app](https://caprae-lead-tool.streamlit.app/)  

---

## 🚀 What this project is
A focused 5-hour demo tool showcasing **lead validation, enrichment, scoring, and prioritization** for B2B prospecting.  

The tool simulates a **production-ready pipeline** with a clean Streamlit UI:  
- ✅ **Email validation** → reduces wasted outreach  
- ✅ **Lead enrichment** → adds company domain + guessed LinkedIn company URL  
- ✅ **Deduplication** → removes duplicate emails/companies  
- ✅ **Lead scoring (0–100)** → with weighted rules for industry & signals  
- ✅ **Priority labels (High/Medium/Low)** → to rank prospects  
- ✅ **Exports** → cleaned CSV + short report (ready for CRM import)  

💡 Goal: **improve lead quality, sales focus, and outreach efficiency.**

---

## 📂 Files in repo
- `main.py` — Streamlit app (UI + processing logic)  
- `requirements.txt` — minimal dependencies  
- `runtime.txt` — Python runtime version (for Streamlit Cloud)  
- `Sample_Output.csv` — example processed dataset  
- `Report.txt` — example generated report  
- `Test_dataset.csv` — test dataset for demo  
- `README.md` — this file  

---

## ▶️ How to run locally
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

👨‍💻 Built by **Shreerama D S** as part of Caprae Capital’s recruiting assignment.  

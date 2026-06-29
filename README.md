# DeltaCodes

AI-assisted policy change detection for healthcare regulatory management.

With regular changes in healthcare policies across different sources (e,g. CPT, CMS, and payer-specific sources) massive bottlenecks exist where 
analysts compare versions manually. DeltaCodes comes handy in this process as it detects what changed, classifies each change, flags ambiguities that need human review. It then creates outputs of a structured JSON that downstream systems can consume.

The tool does not make reimbursement decisions and does not aim for full AI automation. It helps analysts to deep dive into what changed, what are uncertainties, what requires further interpretation, and what should be update in the system.

---

## How It Works

```
PDF v1 + PDF v2
      |
pdfplumber extracts raw text from both documents
      |
Both texts are sent to Gemini (AI) with a structured prompt
      |
Gemini (AI) returns a classified JSON:
  - change type, confidence level, impact rating per change
  - ambiguous clauses flagged for human review
  - plain English summary and analyst notes
      |
Streamlit renders the results:
  - summary box
  - classified changes table
  - ambiguity warnings
  - analyst notes
  - JSON download for audit trail or downstream pipeline use
```

The JSON output is designed to create a handoff artifact that's machine readable, timestamped, and appendable as the change moves through review (regular audits included) and into production rule updates.

---

## Project Structure

```
deltacodes/
├── app.py                  # Streamlit frontend
├── pipeline/
│   ├── pdf_parser.py       # PDF text extraction via pdfplumber
│   └── llm_analyzer.py     # Gemini API call and JSON parsing
├── sample_docs/            # CMS Stark Law CPT/HCPCS update PDFs
├── output/                 # Generated JSON reports
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
```

Add a `.env` file in the root directory:

```
GEMINI_API_KEY= {ENTER YOUR KEY HERE}
```

Run the app:

```bash
streamlit run app.py
```

---

## Usage

1. Upload the old policy PDF on the left and the new version on the right
2. Click Run Analysis
3. Review the classified changes, ambiguity flags, and analyst notes
4. Download the JSON report for audit records or downstream use

---

## Output Format

```json
{
  "summary": "plain English summary of what changed",
  "classified_changes": [
    {
      "code": "77401",
      "change_type": "deleted",
      "description": "Code 77401 was removed from Radiation Therapy Services",
      "confidence": "high",
      "impact": "high"
    }
  ],
  "ambiguities": [
    {
      "text": "the ambiguous clause",
      "reason": "why a human must review this before it moves downstream"
    }
  ],
  "review_status": "human_review_required",
  "analyst_notes": "follow-up actions and cross-references for the reviewing analyst"
}
```

`review_status` is one of `auto_approved`, `human_review_required`, or `escalate_immediately`. Ambiguous or low-confidence changes are never auto-approved.

---

## Why JSON

The structured output serves as an audit trail. Each run captures what changed, the confidence level, and the review status. When an analyst approves the changes, you append who reviewed it and when. 

---

## Sample Documents

The `sample_docs` folder includes CMS Physician Self-Referral Law CPT/HCPCS code list updates from 2023 through 2026, sourced from cms.gov. These are used as the default demo pair.

---

## Dependencies

- pdfplumber
- google-genai
- streamlit
- python-dotenv

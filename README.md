# 📄 Document Analyst

**The smart friend who actually reads your documents.**

Upload a contract, lease, research paper, offer letter, or assignment brief and get an
instant, plain-English breakdown — a safety score, a structured summary, red-flag warnings,
and answers to any question you ask about the document.

Powered by [Groq](https://groq.com/) running Meta's `llama-3.3-70b-versatile` model.

---

## ✨ Features

- **Automatic document detection** — identifies the document type (contract, lease, research paper, offer letter, etc.) the moment you upload.
- **Safety & clarity score** — a 1–10 rating with a quick verdict (*Safe to proceed* / *Proceed with caution* / *Review carefully*).
- **📝 Summarize** — structured summary of key points, obligations, dates, and numbers.
- **💡 Explain Simply** — a plain-English, section-by-section explanation with no legal or technical jargon.
- **🚩 Scan for Red Flags** — flags risky clauses as HIGH or MEDIUM risk and tells you what to do.
- **❓ What Should I Ask?** — the most important questions to ask before signing or agreeing.
- **💬 Ask anything** — free-form Q&A grounded only in your document's content.
- **✍️ Response drafts** *(web version)* — generate a ready-to-edit email/note to raise a concern with the other party.

---

## 🗂️ Project structure

This repo ships **two independent implementations** of the same tool:

| File | Description |
|------|-------------|
| `app.py` | **Streamlit** app. Supports **PDF and Word (`.docx`)**. Runs the Groq API server-side using a key from your environment. |
| `index.html` | **Standalone browser** app. PDF only (via [pdf.js](https://mozilla.github.io/pdf.js/)). No build step, no backend — open it in a browser. |
| `requirements.txt` | Python dependencies for the Streamlit app. |

---

## 🚀 Getting started (Streamlit app)

### 1. Clone the repo

```bash
git clone https://github.com/tanushreetiwari59/Test.git
cd Test
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies: `streamlit`, `PyPDF2`, `python-docx`, `groq`, `python-dotenv`.

### 3. Add your Groq API key

Create a `.env` file in the project root (it's already git-ignored):

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key from the [Groq Console](https://console.groq.com/keys).

### 4. Run the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## 🌐 Running the browser version (`index.html`)

The standalone version needs no install — just open `index.html` in any modern browser
(or host it on GitHub Pages / any static host).

> **⚠️ Important:** `index.html` currently calls the Groq API **directly from the browser**,
> which requires the API key to be present in the client-side code. **Never commit a real API key
> to a public repository.** Before deploying this version, rotate the existing key and route
> requests through a small backend or serverless proxy so the key is never exposed to users.

---

## 🔐 Privacy & security

- Documents are **not stored** on any server by this project.
- Document text **is sent to Groq's API** for analysis — see [Groq's privacy policy](https://groq.com/privacy-policy/) for data-retention details.
- Only the first ~10,000 characters of a document are sent to the model.
- **Image-based / scanned PDFs are not supported** — the text must be selectable.

---

## 🛠️ Tech stack

- **Model:** `llama-3.3-70b-versatile` via the Groq API
- **Backend app:** Python + Streamlit
- **PDF parsing:** PyPDF2 (Python) / pdf.js (browser)
- **Word parsing:** python-docx (Python)
- **Frontend:** Vanilla HTML / CSS / JavaScript

---

## 📌 Limitations

- Works only with **text-based** documents (no OCR for scanned images).
- Analysis is limited to the first ~10,000 characters of long documents.
- AI output is for **guidance only** — it is **not legal, financial, or professional advice**. Always consult a qualified professional for important decisions.

---

## 📄 License

No license file is currently included. Add one (e.g. [MIT](https://choosealicense.com/licenses/mit/)) if you intend others to reuse this code.

<div align="center">

# 📄 Document Analyst 🔍

### The smart friend who actually reads your documents.

Upload a contract, lease, research paper, or offer letter and get an instant,
plain-English breakdown — a safety score, a structured summary, red-flag warnings,
and answers to any question you ask — powered by **your** Groq key, with **your**
documents never stored on a server.

[![Groq](https://img.shields.io/badge/Powered%20by-Groq-f55036)](https://groq.com)
[![Llama 3.3 70B](https://img.shields.io/badge/Model-Llama%203.3%2070B-0467df)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3-3776ab)](https://www.python.org)
[![BYOK](https://img.shields.io/badge/BYOK-Bring%20Your%20Own%20Key-success)](#-set-an-api-key)

</div>

---

## 🌟 Vision

Every important moment in life comes with a document — and most of them are long, dense, and
written by people who are not on your side. Document Analyst turns any PDF or Word file into a
conversation: ask what a clause means, get the red flags before you sign, or summarize a 40-page
paper in under a minute.

Three principles guide it:

1. **Understanding should be instant.** Upload and the document is already detected, scored, and ready — before you click anything.
2. **Your documents are yours.** No accounts, no storage, no tracking. Text goes only to the AI provider you chose, and nothing is kept.
3. **It should speak human.** No legalese, no jargon — just clear answers and concrete next steps.

---

## 🌱 Core Values

🔑 **BYOK by design** — Bring your own [Groq](https://console.groq.com/keys) API key. The Streamlit app reads it from a local `.env`; the browser app asks for it at runtime and keeps it only in your tab. No hosted backend, no shared key.

🧠 **Grounded in your document** — Every answer uses **only** the text of the file you uploaded. The AI is instructed to ignore outside knowledge, so it summarizes what is actually there — not what it assumes.

🛡️ **Privacy as the default** — Documents are never stored on a server. The only network call is the analysis request you initiate, sent to Groq's API.

🪶 **Built for one job** — Not a general chatbot. Every feature exists to help you understand a document and decide what to do next.

---

## ❓ Why This Exists

A landlord sends a 20-page lease at 10pm before move-in day. A client emails a contract full of
clauses you've never seen. A professor assigns a 40-page paper due tomorrow. In each case the cost
of *not* understanding is real — a missed penalty clause, a bad deal, a wasted week. Document
Analyst exists to close that gap in 60 seconds, without you having to become a lawyer, an analyst,
or a speed-reader.

---

## ✨ Features

| | |
|---|---|
| 🏷️ **Auto-detection** | Identifies the document type (contract, lease, research paper, offer letter, assignment brief…) the moment you upload. |
| 📊 **Safety score** | A 1–10 clarity-and-safety rating with a quick verdict — *Safe to proceed*, *Proceed with caution*, or *Review carefully*. |
| 📝 **Summarize** | Structured summary of key points, obligations, dates, and numbers — ending with concrete next steps. |
| 💡 **Explain simply** | A plain-English, section-by-section walkthrough with no legal or technical jargon. |
| 🚩 **Scan for red flags** | Flags risky clauses as **HIGH** or **MEDIUM** risk and tells you exactly what to do about each. |
| ❓ **What should I ask?** | The most important questions to raise before signing or agreeing, most critical first. |
| 💬 **Ask anything** | Free-form Q&A grounded only in your document's content. |
| ✍️ **Response drafts** | *(browser app)* Generate a ready-to-edit email or note to raise a concern with the other party. |

---

## 🏗️ How It Works

```
┌──────────────────┐    selectable text    ┌────────────────────┐
│  Your document   │ ─────────────────────▶│  Text extraction   │
│  (PDF / DOCX)    │   first ~10k chars    │ PyPDF2 · pdf.js    │
└──────────────────┘                       └─────────┬──────────┘
                                                     │ prompt + document
                                                     ▼
                                          ┌──────────────────────┐
                                          │     Groq API         │
                                          │  llama-3.3-70b       │
                                          └──────────┬───────────┘
                                                     │ analysis
                                                     ▼
                              detected type · safety score · summary ·
                              red flags · answers · response drafts
```

The document is detected and scored on upload; each action sends the document text plus a focused
prompt to the model and renders the result. Only the first ~10,000 characters are sent.

**Project layout**

```
app.py            Streamlit app — PDF + Word (.docx), key from .env
index.html        Standalone browser app — PDF via pdf.js, BYOK at runtime
requirements.txt  Python dependencies
.env              GROQ_API_KEY (git-ignored, you create this)
```

---

## 🚀 Getting Started

**Prerequisites:** Python 3, `pip`, and a free [Groq API key](https://console.groq.com/keys).

```sh
# clone the repo
git clone https://github.com/tanushreetiwari59/Test.git
cd Test

# install dependencies
pip install -r requirements.txt

# run the Streamlit app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

> **Prefer zero install?** Just open `index.html` in any modern browser — no Python, no build step. It runs entirely client-side and asks for your Groq key when you first analyse a document.

---

## 🔑 Set An API Key

**Streamlit app (`app.py`)** — create a `.env` file in the project root (it's git-ignored):

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Browser app (`index.html`)** — no file needed. The app prompts for your key on first use and stores it only in that browser tab's `sessionStorage`; it is never committed or sent anywhere except Groq.

> Get a free key from the [Groq Console](https://console.groq.com/keys). Treat it like a password — never commit a real key to a public repository.

---

## 📋 Two Ways To Run

| | Streamlit app | Browser app |
|---|---|---|
| **File** | `app.py` | `index.html` |
| **Formats** | PDF **and** Word (`.docx`) | PDF only |
| **Setup** | `pip install` + `.env` | Open the file — no install |
| **Key handling** | Server-side from `.env` | Entered at runtime, tab-only |
| **Best for** | Local/private use | Quick sharing & static hosting |

---

## 🛡️ Privacy

- **No backend storage.** Your document is never saved to a server by this project.
- **Sent only to Groq.** Document text is sent to Groq's API for analysis — see [Groq's privacy policy](https://groq.com/privacy-policy/) for data-retention details.
- **Limited payload.** Only the first ~10,000 characters of a document are sent.
- **Text-based only.** Scanned/image PDFs are not supported — the text must be selectable.

---

## 🧱 Tech Stack

**Groq** (`llama-3.3-70b-versatile`) · **Python** + **Streamlit** · **PyPDF2** & **python-docx** · **pdf.js** · vanilla **HTML / CSS / JavaScript**.

---

## ⚠️ Disclaimer

Document Analyst provides **AI-generated guidance only**. It is **not** legal, financial, or
professional advice. Always consult a qualified professional before making important decisions
based on a document.

<div align="center">

**Built for people who have to sign things they didn't write.**

</div>

---

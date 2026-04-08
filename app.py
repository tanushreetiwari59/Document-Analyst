import streamlit as st
import PyPDF2
import docx
import io
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("GROQ_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Document Analyst",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>
* { font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
.stApp { background: #ffffff !important; }
.block-container { max-width: 720px !important; padding: 2rem 1rem !important; }
#MainMenu, footer, header { visibility: hidden; }

.top-header { text-align: center; padding: 20px 0 8px; }
.top-logo { font-family: Georgia, serif; font-size: 22px; color: #111; font-weight: 400; margin-bottom: 4px; }
.top-tag { font-size: 12px; color: #aaa; letter-spacing: 0.05em; }

.detected-box {
    background: #eef2ff; border: 1px solid #c7d2fe;
    border-radius: 8px; padding: 10px 16px;
    display: flex; align-items: center;
    justify-content: space-between; margin-bottom: 12px;
}
.score-box {
    background: #fff; border: 1px solid #f0f0f0;
    border-radius: 12px; padding: 24px;
    text-align: center; margin-bottom: 16px;
}
.result-box {
    background: #fff; border: 1px solid #efefef;
    border-radius: 14px; padding: 24px; margin: 16px 0;
    text-align: left;
}
.risk-high {
    background: #fff8f8; border-left: 3px solid #ef4444;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 10px;
}
.risk-medium {
    background: #fffbf0; border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0; padding: 12px 16px; margin-bottom: 10px;
}
.next-steps {
    background: #f0f0ff; border-radius: 8px;
    padding: 14px 16px; margin-top: 12px;
}
.stButton > button {
    background: #fafafa !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    color: #555 !important;
    font-size: 13px !important;
    padding: 12px !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: #c7d2fe !important;
    color: #4338ca !important;
    background: #fafeff !important;
}
div[data-testid="stFileUploader"] section {
    border: 1.5px dashed #c7d2fe !important;
    border-radius: 12px !important;
    background: #fafbff !important;
    padding: 20px !important;
}
.stTextInput > div > div > input {
    border: 1px solid #e8e8e8 !important;
    border-radius: 8px !important;
    font-size: 13px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="top-header">
    <div class="top-logo">Document Analyst</div>
    <div class="top-tag">The smart friend who actually reads your documents.</div>
</div>
""", unsafe_allow_html=True)

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(io.BytesIO(file.read()))
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def analyse_document(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""Analyse this document and reply in EXACTLY this format:

TYPE: [document type in 3 words max — choose from: Contract, Research Paper, Lease Agreement, Job Offer Letter, Academic Paper, Financial Document, Policy Document, Assignment Brief, Case Study, General Document. If it contains tasks or evaluation criteria it is Assignment Brief NOT Job Offer Letter]
SCORE: [number 1-10 for safety and clarity]
REASON: [max 10 words explaining the score]

Document: {text[:3000]}"""
        }]
    )
    result = response.choices[0].message.content
    doc_type = "General Document"
    score = 7
    reason = "Document analysed"
    for line in result.strip().split('\n'):
        if line.startswith('TYPE:'):
            doc_type = line.replace('TYPE:', '').strip()
        if line.startswith('SCORE:'):
            try: score = int(line.replace('SCORE:', '').strip())
            except: score = 7
        if line.startswith('REASON:'):
            reason = line.replace('REASON:', '').strip()
    return doc_type, score, reason

def ask_ai(doc_text, prompt, doc_type):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"""You are an expert analyst reviewing a {doc_type}.
Use ONLY the document content provided.
Be clear, direct and well structured.
Use bullet points where helpful.
Always end with a NEXT STEPS section.
Document: {doc_text}"""},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1200
    )
    return response.choices[0].message.content

uploaded_file = st.file_uploader(
    "Upload your document — PDF or Word",
    type=["pdf", "docx"]
)

if uploaded_file:
    with st.spinner("Reading your document..."):
        if uploaded_file.name.endswith(".pdf"):
            doc_text = extract_text_from_pdf(uploaded_file)
        else:
            doc_text = extract_text_from_docx(uploaded_file)

    if not doc_text.strip():
        st.error("Could not read this document. It may be a scanned image PDF. Please try a text-based PDF.")
        st.stop()

    doc_text = doc_text[:10000]

    with st.spinner("Analysing your document..."):
        doc_type, score, reason = analyse_document(doc_text)

    color = "#4338ca" if score >= 7 else "#f59e0b" if score >= 5 else "#ef4444"
    verdict = "Safe to proceed" if score >= 7 else "Proceed with caution" if score >= 5 else "Review carefully"

    st.markdown(f"""
    <div class="detected-box">
        <div>
            <div style="font-size:12px;color:#4338ca;font-weight:500;">📋 {doc_type} detected</div>
            <div style="font-size:10px;color:#a5b4fc;margin-top:2px;">Identified automatically</div>
        </div>
        <div style="font-size:10px;color:#a5b4fc;">✓ Ready to analyse</div>
    </div>
    <div class="score-box">
        <div style="font-size:48px;font-weight:700;color:{color};line-height:1;margin-bottom:6px;">{score}<span style="font-size:20px;color:#ddd;font-weight:400;">/10</span></div>
        <div style="font-size:12px;color:#999;margin-bottom:12px;">{verdict}</div>
        <div style="background:#f0f0f0;border-radius:6px;height:5px;width:100%;margin-bottom:8px;">
            <div style="background:{color};height:5px;border-radius:6px;width:{score*10}%;"></div>
        </div>
        <div style="font-size:11px;color:#ccc;">{reason}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### What would you like to do?")
    col1, col2 = st.columns(2)

    with col1:
        summarize = st.button("📝  Summarize Document")
        red_flags = st.button("🚩  Scan for Red Flags")
    with col2:
        explain = st.button("💡  Explain Simply")
        what_to_ask = st.button("❓  What Should I Ask?")

    if summarize:
        with st.spinner("Summarizing..."):
            result = ask_ai(doc_text,
                f"Give a structured summary of this {doc_type}. Cover key points, main obligations or findings, important dates or numbers, and what this means for the reader. End with NEXT STEPS.",
                doc_type)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    if red_flags:
        with st.spinner("Scanning for red flags..."):
            result = ask_ai(doc_text,
                f"Scan this {doc_type} for red flags. For each one label it HIGH RISK or MEDIUM RISK, explain why it is risky, and say what to do. End with NEXT STEPS.",
                doc_type)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    if explain:
        with st.spinner("Simplifying..."):
            result = ask_ai(doc_text,
                f"Explain this {doc_type} in plain English like you are talking to someone with no legal or technical background. End with NEXT STEPS.",
                doc_type)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    if what_to_ask:
        with st.spinner("Thinking of smart questions..."):
            result = ask_ai(doc_text,
                f"What are the most important questions a regular person should ask before agreeing to this {doc_type}? List most critical first. End with NEXT STEPS.",
                doc_type)
        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 💬 Ask anything about your document")
    question = st.text_input("", placeholder="e.g. What are the payment terms?")

    if question:
        with st.spinner("Finding your answer..."):
            answer = ask_ai(doc_text, question, doc_type)
        st.markdown(f'<div class="result-box">{answer}</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:40px 20px;color:#ccc;font-size:13px;">
        Upload a PDF or Word document above to get started<br>
        <span style="font-size:11px;">Contracts · Research Papers · Lease Agreements · Offer Letters · and more</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:24px;color:#ddd;font-size:11px;border-top:1px solid #f5f5f5;margin-top:40px;">
    Document Analyst · The smart friend who actually reads your documents.
</div>
""", unsafe_allow_html=True)

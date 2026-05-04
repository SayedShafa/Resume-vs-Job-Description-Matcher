import streamlit as st
import re
import os
from PyPDF2 import PdfReader
import docx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import skills_list        #Outside file from where skills will be imported

#-------------------------Text Extract

def extract_text_from_pdf(file):
    
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(file):
     
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# ---------------------------Skill Extract
def extract_skills(text, skills_list):
    """
    Extract skills from a given text based on a predefined skills list.
    Returns a set of found skills.
    """
    text = text.lower()
    found = set()
    for skill in skills_list:
        # Search for the skill as a whole word (word boundary)
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
    return found

# -------------------------------Similarity Metrics
def jaccard_similarity(set1, set2):
    if not set1 and not set2:
        return 0.0
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union) * 100

def compute_cosine_similarity(text1, text2):
    """Compute Cosine Similarity between two texts using TF-IDF vectors.
    Returns a percentage."""

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform([text1, text2])
    sim = cosine_similarity(tfidf[0], tfidf[1])[0][0]
    return sim * 100

def semantc_similarity(text1, text2):
    """Compute Semantic Similarity between two texts using Sentence-BERT.
    Returns a percentage."""
    model = SentenceTransformer('all-MiniLM-L6-v2')  # leightweight pretained mod
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    sim = util.cos_sim(emb1, emb2).item()
    return sim * 100

# ---------------- Interface
st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("📄 Resume vs Job Description Matcher")
st.markdown("Upload your CV and paste the job description to see the skill match percentage and missing skills.")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("CV (PDF or DOCX)", type=["pdf", "docx"])
with col2:
    jd_text = st.text_area("Job Description", height=300, placeholder="Paste the job description here...")

if uploaded_file and jd_text:
    # Extract raw text from the uploaded CV
    if uploaded_file.type == "application/pdf":
        cv_text = extract_text_from_pdf(uploaded_file)
    else:
        cv_text = extract_text_from_docx(uploaded_file)

    # Extract skills from CV and Job Description
    cv_skills = extract_skills(cv_text, skills_list.SKILLS)
    jd_skills = extract_skills(jd_text, skills_list.SKILLS)

    # Calculate match percentage using Jaccard similarity
    match_percent = jaccard_similarity(cv_skills, jd_skills)

    # Additional metrics (optional)
    cosine_sim = compute_cosine_similarity(cv_text, jd_text)
    semantic_sim = semantc_similarity(cv_text, jd_text)

    # Display Result
    st.subheader("Match Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Skill Match (Jaccard)", f"{match_percent:.1f}%")
    c2.metric("Cosine Similarity", f"{cosine_sim:.1f}%")
    c3.metric("Semantic Similarity", f"{semantic_sim:.1f}%")

    st.subheader(" Skills Found in CV")
    st.write(", ".join(sorted(cv_skills)) if cv_skills else "None found")
    st.subheader(" Required Skills in JD")
    st.write(", ".join(sorted(jd_skills)) if jd_skills else "None found")

    missing = jd_skills - cv_skills
    if missing:
        st.subheader(" Missing Skills")
        st.write(", ".join(sorted(missing)))
    else:
        st.success("All required skills present in CV!")


#streamlit run cv_selection_main.py
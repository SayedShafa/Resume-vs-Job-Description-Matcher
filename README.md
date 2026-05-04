# Resume vs Job Description Matcher 
---
Resume vs Job Description Matcher is an NLP-powered tool that analyzes a candidate's CV (PDF/DOCX) and compares it with a job description to calculate a match percentage. It extracts relevant skills from both documents using keyword matching, and also provides additional similarity metrics (Cosine and Semantic) for a comprehensive evaluation. The goal is to help recruiters or job seekers quickly assess the suitability of a resume for a specific role.

---
<img width="1504" height="633" alt="image" src="https://github.com/user-attachments/assets/0d503dd6-3c3a-447e-817b-9c48b5d494ff" />

---
### Features:

- Upload CV in PDF or DOCX format.

- Paste any job description text.

- Automatic skill extraction using a customizable skill list.

- **Jaccard Similarity** for precise skill overlap percentage.

- **Cosine Similarity** (TF-IDF based) for overall text alignment.

- **Semantic Similarity** (Sentence-BERT) to capture contextual meaning.

- Highlights missing skills from the CV.

- Clean, interactive web interface built with Streamlit.

**Resume vs Job Description Matcher**
- cv_selection_main.py--------- Main Streamlit application
- skills_list.py---------- Customizable skill keywords list
- requirements.txt ----- Python dependencies
- README.md ---------------Project documentation
- resume.docs ------------- sample of a cv
- job_destription.txt  --------sample of a job description


### Technologies Used:
- Python
- Streamlit (for interface)
- PyPDF2(PDF text extraction)
- python-docx (DOCX text extraction)
- scikit-learn(TF-IDF, cosine similarity)
- Sentence-Transformers
- regex

### How to Run:

- Install dependencies: pip install -r requirements.txt

- Run the app: streamlit run cv_selection_main.py

- Open http://localhost:8501/ in your browser.

### Usage
- Upload a CV file in PDF or DOCX format.

- Paste the text of a job description into the text area.

### View the results:

- Match Summary – Jaccard, Cosine, and Semantic similarity scores.

- Skills Found in CV – list of extracted skills from the resume.

- Required Skills in JD – list of skills mentioned in the job description.

- Missing Skills – skills present in JD but absent in CV.

### Customization
You can easily modify the skills that the tool looks for by editing the skills_list.py file. Simply add or remove keywords from the SKILLS list.

SKILLS = [
    "python",
    "java",
    "machine learning",
    "docker",
    ...
]
- You can also define multiple skill lists for different domains (e.g., tech_skills.py, soft_skills.py) and import them accordingly.

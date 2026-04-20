import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("AI Resume Analyzer")
st.write("Upload your resume and get instant AI feedback 🚀")

uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])


def extract_text(file):
    if file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
        return text
    else:
        return file.read().decode("utf-8", errors="ignore")


def analyze_resume(text):
    score = 0
    feedback = []

    text_lower = text.lower()

    # Skill keywords
    keywords = [
        "python", "sql", "machine learning", "power bi",
        "data analysis", "excel", "pandas", "numpy",
        "scikit", "visualization"
    ]

    for word in keywords:
        if word in text_lower:
            score += 10
        else:
            feedback.append(f"Add or highlight skill: {word}")

    # Project check
    if "project" not in text_lower:
        feedback.append("Add a Projects section with real work")

    # Experience check
    if "experience" not in text_lower:
        feedback.append("Add Experience or Internship details")

    # Resume length check
    word_count = len(text.split())
    if word_count < 150:
        feedback.append("Resume is too short (add more details)")
    elif word_count > 600:
        feedback.append("Resume is too long (keep it concise)")

    # Normalize score
    score = min(score, 100)

    return score, feedback


if uploaded_file:
    content = extract_text(uploaded_file)

    st.subheader("Resume Content")
    st.write(content)

    score, feedback = analyze_resume(content)

    st.subheader("Score")
    st.progress(score)
    st.write(f"{score}/100")

    st.subheader("Suggestions")

    if feedback:
        for f in feedback:
            st.write("•", f)
    else:
        st.success("Great Resume! No major improvements needed 🎉")
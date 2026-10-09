```python
import streamlit as st
import fitz
import re

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #d8b4fe, #f5d0fe, #e9d5ff);
}

h1 {
    text-align: center;
    color: #4c1d95;
}

.section-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.score-box {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📄 Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

# ---------------- RESUME UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📂 Upload your resume",
    type=["pdf"]
)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


# ---------------- SKILL FINDING ----------------
def find_skills(text):

    skills = [
        "python",
        "c++",
        "java",
        "javascript",
        "html",
        "css",
        "sql",
        "mysql",
        "mongodb",
        "react",
        "node.js",
        "streamlit",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "data analysis",
        "pandas",
        "numpy",
        "matplotlib",
        "git",
        "github",
        "excel",
        "communication",
        "problem solving",
        "teamwork",
        "leadership"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills


# ---------------- JOB DESCRIPTION SUMMARY ----------------
def summarize_job_description(job_description):

    # Remove extra spaces
    text = re.sub(r"\s+", " ", job_description).strip()

    # If description is short
    if len(text) <= 250:
        return text

    # Take first meaningful part and create a short summary
    sentences = re.split(r'(?<=[.!?])\s+', text)

    summary = ""

    for sentence in sentences:
        if len(summary) + len(sentence) <= 450:
            summary += sentence + " "
        else:
            break

    summary = summary.strip()

    if not summary:
        summary = text[:450] + "..."

    return summary


# ---------------- ANALYZE BUTTON ----------------
if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    st.markdown(
        '<div class="section-box">',
        unsafe_allow_html=True
    )

    st.subheader("📃 Extracted Resume Text")
    st.write(resume_text)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SKILLS ----------------
    found_skills = find_skills(resume_text)

    st.markdown(
        '<div class="section-box">',
        unsafe_allow_html=True
    )

    st.subheader("🛠️ Skills Found")

    if found_skills:
        st.write(", ".join(found_skills))
    else:
        st.write("No known skills found.")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- JOB DESCRIPTION ----------------
    st.markdown(
        '<div class="section-box">',
        unsafe_allow_html=True
    )

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here:",
        height=250
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ANALYZE ----------------
    if st.button("🔍 Analyze Resume"):

        if job_description.strip() == "":
            st.warning("Please enter a job description.")
        else:

            # ---------------- JOB DESCRIPTION SUMMARY ----------------
            summary = summarize_job_description(job_description)

            st.markdown(
                '<div class="section-box">',
                unsafe_allow_html=True
            )

            st.subheader("📝 Job Description Summary")

            st.write(summary)

            st.markdown("</div>", unsafe_allow_html=True)

            # ---------------- JOB DESCRIPTION SKILLS ----------------
            job_skills = find_skills(job_description)

            # ---------------- MATCHED SKILLS ----------------
            matched_skills = []

            for skill in found_skills:
                if skill.lower() in [x.lower() for x in job_skills]:
                    matched_skills.append(skill)

            # ---------------- MISSING SKILLS ----------------
            missing_skills = []

            for skill in job_skills:
                if skill.lower() not in [x.lower() for x in found_skills]:
                    missing_skills.append(skill)

            # ---------------- MATCHED SKILLS DISPLAY ----------------
            st.markdown(
                '<div class="section-box">',
                unsafe_allow_html=True
            )

            st.subheader("✅ Matched Skills")

            if matched_skills:
                st.write(", ".join(matched_skills))
            else:
                st.write("No matched skills found.")

            st.markdown("</div>", unsafe_allow_html=True)

            # ---------------- MISSING SKILLS DISPLAY ----------------
            st.markdown(
                '<div class="section-box">',
                unsafe_allow_html=True
            )

            st.subheader("❌ Missing Skills")

            if missing_skills:
                st.write(", ".join(missing_skills))
            else:
                st.write("No missing skills.")

            st.markdown("</div>", unsafe_allow_html=True)

            # ---------------- ATS SCORE ----------------
            if len(job_skills) > 0:

                ats_score = (
                    len(matched_skills) / len(job_skills)
                ) * 100

            else:
                ats_score = 0

            ats_score = round(ats_score, 2)

            # ---------------- ATS DISPLAY ----------------
            st.markdown(
                '<div class="score-box">',
                unsafe_allow_html=True
            )

            st.subheader("📊 ATS Match Score")

            st.metric(
                label="Resume Match",
                value=f"{ats_score}%"
            )

            if ats_score >= 80:
                st.success(
                    "🎉 Excellent match! Your resume matches most of the required skills."
                )

            elif ats_score >= 60:
                st.info(
                    "👍 Good match! You can improve your resume by adding some missing skills."
                )

            else:
                st.warning(
                    "⚠️ Low match. Consider improving your resume according to the job requirements."
                )

            st.markdown("</div>", unsafe_allow_html=True)

            # ---------------- SUGGESTIONS ----------------
            st.markdown(
                '<div class="section-box">',
                unsafe_allow_html=True
            )

            st.subheader("💡 Suggestions")

            if missing_skills:

                st.write(
                    "Consider adding these relevant skills to your resume if you actually have them:"
                )

                st.write(", ".join(missing_skills))

            else:

                st.write(
                    "Your resume contains all the detected skills mentioned in the job description."
                )

            st.markdown("</div>", unsafe_allow_html=True)
```
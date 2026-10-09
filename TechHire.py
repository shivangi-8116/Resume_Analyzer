import streamlit as st
import fitz

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #667eea, #764ba2);
    }

    h1 {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
    }

    [data-testid="stFileUploader"] {
        background-color: rgba(255, 255, 255, 0.15);
        padding: 15px;
        border-radius: 12px;
    }

    textarea {
        border-radius: 12px !important;
    }

    .score-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 35px;
        font-weight: bold;
        background-color: black;
        border: 2px solid #dddddd;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 Resume Analyzer 🚀")
st.write("Upload your resume to analyze it.")

resume = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    label_visibility="collapsed"
)


def extract_text_from_pdf(pdf_file):
    text = ""

    document = fitz.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    for page in document:
        text += page.get_text()

    document.close()

    return text


def find_skills(resume_text):
    skills = [
        "Python",
        "C++",
        "Java",
        "JavaScript",
        "HTML",
        "CSS",
        "SQL",
        "Git",
        "Machine Learning",
        "Data Science",
        "Streamlit",
        "React",
        "Node.js",
        "MongoDB",
        "MySQL",
        "NumPy",
        "Pandas",
        "TensorFlow",
        "PyTorch",
        "Scikit-learn"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)

    return found_skills


def compare_skills(resume_skills, job_skills):
    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


def calculate_match_score(matched_skills, job_skills):
    if len(job_skills) == 0:
        return 0

    score = (
        len(matched_skills) /
        len(job_skills)
    ) * 100

    return score


def give_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            "Consider adding "
            + skill
            + " to your resume if you have this skill."
        )

    return suggestions


def summarize_job_description(job_description):
    sentences = job_description.replace("\n", " ").split(".")
    summary = []

    for sentence in sentences:
        sentence = sentence.strip()

        if sentence:
            summary.append(sentence)

        if len(summary) == 3:
            break

    return ". ".join(summary) + "."


st.subheader("💼 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    label_visibility="collapsed",
    height=180
)


if st.button("🔍 Analyze Resume"):

    if resume is None:
        st.error("Please upload a resume.")

    elif job_description.strip() == "":
        st.error("Please enter a job description.")

    else:

        resume_text = extract_text_from_pdf(resume)

        st.subheader("📄 Extracted Resume Text")

        with st.expander("👁️ View Extracted Text"):
            st.write(resume_text)

        found_skills = find_skills(resume_text)

        st.subheader("🛠️ Skills Found")

        if found_skills:
            for skill in found_skills:
                st.write("✅", skill)
        else:
            st.write("No known skills found.")

        st.subheader("📝 Job Description Summary")

        job_summary = summarize_job_description(job_description)

        st.write(job_summary)

        job_skills = find_skills(job_description)

        matched_skills, missing_skills = compare_skills(
            found_skills,
            job_skills
        )

        st.subheader("✅ Matched Skills")

        if matched_skills:
            for skill in matched_skills:
                st.write("🟢", skill)
        else:
            st.write("No matched skills found.")

        st.subheader("❌ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write("🔴", skill)
        else:
            st.write("No missing skills.")

        match_score = calculate_match_score(
            matched_skills,
            job_skills
        )

        st.subheader("📊 ATS Match Score")

        st.markdown(
            f"""
            <div class="score-box">
                {match_score:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        if match_score >= 80:
            st.success(
                "🎉 Candidate meets the 80% matching threshold — "
                "Recommended for further consideration."
            )
        else:
            st.warning(
                "⚠️ Candidate does not meet the 80% matching threshold."
            )

        suggestions = give_suggestions(missing_skills)

        st.subheader("💡 Suggestions")

        if suggestions:
            for suggestion in suggestions:
                st.info(suggestion)
        else:
            st.success(
                "🎯 Your resume matches all detected job skills!"
            )


st.divider()

st.write(
    "📄 Resume Analyzer | Built with Python & Streamlit 🚀"
)
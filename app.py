import streamlit as st
import fitz #we use fitz becoz streamlit can receive the pdf but doesnt itself extract the text from it 
import re
st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="centered"
)
st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg,#667eea,#764ba2);
}

h1 {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 18px;
}

.section-box {
    padding: 15px;
    border-radius: 12px;
    background-color: white;
    border: 1px solid #dddddd;
    margin-top: 15px;
    margin-bottom: 10px;
    color: black;

}
.section-box h3{
    color: black;
    margin: 0;
}

.score-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    background-color: white;
    border: 2px solid #dddddd;
    color: black;
}
</style>
""",
    unsafe_allow_html=True
)

st.title("Resume Analyzer 🚀")
st.write("upload your resume to analyze it.")

resume=st.file_uploader(
    "upload your resume",
    type=["pdf"]
)
def extract_text_from_pdf(pdf_file):
    text = ""

    document=fitz.open( #fitz pdf ko kholta h
        stream=pdf_file.read(),#stream gives input to fitz
        filetype="pdf"
    )
    for page in document:
        text += page.get_text()
    document.close()
    return text
def find_skills(resume_text):#master list:program in skills ko recognise kr skta h.
    skills=[
        "python",
        "c++",
        "java",
        "javascript",
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
        "Pandas",
        "TensorFlow",
        "PyTorch",
    ] 
    found_skills = []
    for skill in skills:
        if skill.lower() in resume_text.lower():#skills or resume text ko lower case me krega taaki small our capital letter ka prb nahh ho
            found_skills.append(skill)
    return found_skills
def compare_skills(resume_skills,job_skills):
    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)
    return matched_skills,missing_skills

def calculated_match_score(matched_skills,job_skills):
    if len(job_skills) == 0:
        return 0
    score = (len(matched_skills)/ len(job_skills))*100
    return score

def give_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        suggestions.append(
            " consider adding " + skill + " to your resume, if you have this skill."
        )
    return suggestions
def get_job_description_summary(job_description):

    text = " ".join(job_description.split())
    lower_text = text.lower()

    summary = []

    # Experience
    experience_patterns = [
        r'(\d+\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience)',
        r'(experience\s*(?:of)?\s*\d+\+?\s*(?:years?|yrs?))',
        r'(\d+\+?\s*months?\s*(?:of)?\s*experience)'
    ]

    experience_found = None

    for pattern in experience_patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            experience_found = match.group(1)
            break

    if experience_found:
        summary.append(
            f"💼 **Experience:** {experience_found}"
        )
    else:
        summary.append(
            "💼 **Experience:** Not specifically mentioned"
        )
    # Education
    education_words = [
        "b.tech",
        "btech",
        "b.e.",
        "bachelor",
        "computer science",
        "engineering",
        "m.tech",
        "mtech",
        "master"
    ]

    education_found = []

    for word in education_words:
        if word.lower() in lower_text:
            education_found.append(word)

    if education_found:
        education_found = list(
            dict.fromkeys(education_found)
        )
    else:
        summary.append(
            "🎓 **Education:** Not specifically mentioned"
        )
    # Job Role
    role_words = [
        "software developer",
        "software engineer",
        "python developer",
        "web developer",
        "frontend developer",
        "backend developer",
        "full stack developer",
        "data analyst",
        "data scientist",
        "machine learning engineer",
        "developer",
        "engineer"
    ]

    role_found = []

    for role in role_words:
        if role.lower() in lower_text:
            role_found.append(role)

    if role_found:
        role_text = list(
            dict.fromkeys(role_found)
        )

        summary.append(
            "👨‍💻 **Role:** " + ",".join(role_found)
        )
    else:
        summary.append(
            "👨‍💻 **Role:** Not specifically mentioned"
        )
    # Required Skills
    job_skills = find_skills(job_description)

    if job_skills:

        summary.append(
            "🛠️ **Required Skills:** " + ",".join(job_skills)
        )
    else:
        summary.append(
            "🛠️ **Required Skills:** No known skills detected"
        )


    # Preferred Skills
    preferred_words = [
        "preferred",
        "preferably",
        "nice to have",
        "good to have",
        "bonus",
        "plus"
    ]

    preferred_skills = []

    for skill in job_skills:

        position = lower_text.find(
            skill.lower()
        )

        if position != -1:

            nearby_text = lower_text[
                max(0, position - 100):
                position + 150
            ]

            for word in preferred_words:

                if word in nearby_text:
                    preferred_skills.append(skill)
                    break

    if preferred_skills:
        summary.append(
            "⭐ **Preferred Skills:** " + ",".join(dict.fromkeys(preferred_skills)
        )
        )
    # Responsibilities
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    responsibility_words = [
        "responsible",
        "responsibilities",
        "develop",
        "design",
        "build",
        "create",
        "maintain",
        "analyze",
        "manage",
        "implement",
        "test",
        "work with",
        "collaborate"
    ]

    responsibilities = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        for word in responsibility_words:

            if word in sentence_lower:

                if len(sentence.strip()) > 10:
                    responsibilities.append(
                        sentence.strip()
                    )

                break

    if responsibilities:

        summary.append(
            "📋 **Key Responsibilities:**"
        )

        for responsibility in responsibilities[:3]:

            summary.append(
                "- " + responsibility
            )

    else:

        summary.append(
            "📋 **Key Responsibilities:** "
            "Not specifically mentioned"
        )


    return summary, job_skills

st.markdown(
    '<div clas="section-box">'
    '<h3>💼 Job Description</h3>'
    '</div>',
    unsafe_allow_html=True
) 

#st.subheader("job description 🗒️")


job_description = st.text_area(
    "paste the job description here",
    height=180
)            

if st.button("analyze resume"):
    if resume is None:
        st.error("please upload your resume.")

    elif job_description.strip() == "":
         st.error("please enter a job description.")
     
       
    else:
        resume_text=extract_text_from_pdf(resume)

        summary, job_skills = get_job_description_summary(job_description)
        

        st.markdown(
            """
            <div class="section-box">
               <h3>📝 Job Description Summary</h3>
             </div>
            """,
            unsafe_allow_html=True
        )

        for point in summary:
            st.markdown(point)    

    st.markdown(
        '<div class="section-box">'
        '<h3>📄 Extracted Resume Text</h3>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.expander("👁️ View Extracted Text"):
        st.write(resume_text)
            
        #st.subheader("extracted resume text📝")
    
    found_skills= find_skills(resume_text)

    st.markdown(
        '<div class="section-box">'
        '<h3>🛠️ Skills Found</h3>'
        '</div>',
        unsafe_allow_html=True
    )


    if found_skills:
            st.write("," .join(found_skills))
    else:
        st.write("no known skills found.")   

       
        matched_skills,missing_skills = compare_skills(
            found_skills,
            job_skills,
        )
        st.markdown(
            '<div class="section-box">'
            '<h3>✅ Matched Skills</h3>'
            '</div>',
            unsafe_allow_html=True
        )

        if matched_skills:
                st.write("," .join(matched_skills))
        else:
            st.write("no matched skills found.") 
        

        st.markdown(
            '<div class="section-box">'
            '<h3>❌ Missing Skills</h3>'
            '</div>',
            unsafe_allow_html=True
        )
        if missing_skills:
                st.write("," .join(missing_skills))
        else:
            st.write("no missing skills.")   

        match_score = calculated_match_score(
            matched_skills,
            job_skills,
        )
        st.markdown(
            '<div class="section-box">'
            '<h3>📊 ATS Match Score</h3>'
            '</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="score-box">
                {match_score:.2f}%
            </div>
            """,
            unsafe_allow_html=True
        )

        if match_score>=80:
            st.success(
                "🎉 candidate meets the 80% matching threshold-"
                "recommended for further considerations."
            )
        else:
            st.warning(
                "⚠️ candidate does not meet the 80% matching threshold."
            )

            st.markdown(
                '<div class="section-box">'
                '<h3>💡 Suggestions</h3>'
                '<div>',
                unsafe_allow_html=True

            )    

        #st.subheader("💡suggestions")
        suggestions = give_suggestions(missing_skills)

        if suggestions:
            for suggestion in suggestions:
                st.write(suggestion)
        else:
            st.write("your resume matched all detected job skills!💯")

st.divider()
st.write("Resume Analyzer | Build with python & Streamlit")                    


               

            
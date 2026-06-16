import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

# Page title and setup
st.set_page_config(page_title="AI Resume Builder", page_icon="📝", layout="centered")

st.title("📝 AI Resume Builder & Optimizer")
st.write("Fill in your details below to generate professional resume content using AI!")

st.markdown("---")

# User Input Form
with st.form("resume_form"):
    st.subheader("Personal & Professional Details")
    
    name = st.text_input("Full Name", placeholder="e.g., Saakshi Sharma")
    email = st.text_input("Email Address", placeholder="your.email@example.com")
    skills = st.text_area("Your Skills (Comma separated)", placeholder="e.g., Python, Bioinformatics, Data Analysis")
    experience = st.text_area("Work Experience / Academic Projects", placeholder="Briefly describe your roles, responsibilities, or projects...")
    
    # Form submit button
    submitted = st.form_submit_button("Generate Professional Content")

if submitted:
    if not name or not skills:
        st.warning("Please enter at least your Name and Skills to proceed!")
    else:
        with st.spinner("AI is crafting your professional resume content... Please wait!"):
            try:
                # Initialize Gemini Client (Picks GEMINI_API_KEY from .env)
                client = genai.Client()
                
                # Smart Prompt drafting for accurate profiling
                prompt = f"""
                You are an expert resume writer. Create highly professional, ATS-optimized bullet points for a resume based on these details:
                Name: {name}
                Email: {email}
                Skills: {skills}
                Projects/Experience: {experience}
                
                Strict Formatting & Profile Guidelines:
                1. Ensure the name spelling matches exactly as provided: "{name}".
                2. Maintain an accurate and honest representation of technical skills. If coding languages like Python or R are mentioned alongside biological science/bioinformatics skills, position the candidate as an adaptable, dedicated learner with solid foundational knowledge rather than an advanced expert software developer.
                
                Provide:
                - A strong, compelling Professional Summary.
                - Structured bullet points for Projects/Experience using impactful action verbs.
                - A well-organized Core Skills section.
                """
                
                # Primary Attempt with gemini-2.5-flash
                try:
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                except Exception as primary_error:
                    # Fallback Attempt with stable gemini-1.5-flash if 2.5 is overloaded
                    st.info("Primary server is busy. Switching to backup stable AI engine...")
                    response = client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt,
                    )
                
                # Store text in session state for downloading
                st.session_state['generated_resume'] = response.text
                st.session_state['user_name'] = name
                
                st.success("✨ Your AI-Optimized Resume Content is Ready!")
                st.markdown("### 📄 Generated Content:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Something went wrong! Please check your API key setup or try again in a few moments. Error details: {e}")

# Clean Download Button Section
if 'generated_resume' in st.session_state:
    st.markdown("---")
    st.subheader("📥 Export Your Content")
    st.download_button(
        label="Download Content as Text File",
        data=st.session_state['generated_resume'],
        file_name=f"{st.session_state['user_name']}_AI_Resume.txt",
        mime="text/plain"
    )
    
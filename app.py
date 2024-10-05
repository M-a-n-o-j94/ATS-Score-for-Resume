# Set up the Local Environment
from dotenv import load_dotenv
load_dotenv()  # setup local environment
import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# Initialize Google Generative AI API

google_api = os.getenv("Manoj-Api-Key")
genai.configure(api_key=google_api)
model = genai.GenerativeModel("gemini-pro")

# Function to read PDF content
def read_pdf(pdf):
    reader = PdfReader(pdf)
    resume_text = ""  # Initialize resume content as an empty string
    for page in reader.pages:
        content = page.extract_text()
        if content:
            resume_text += content  # Append content of each page to resume_text
    return resume_text

# Function to analyze the resume and job description
def read_analyse(resume, job_description):
    prompt = f'''Assume yourself as the expert in hiring and recruitment.
    Analyse the resume:
    Resume: {resume}
    
    Compare it with the following job description:
    Job description: {job_description}
    
    Calculate an ATS (Applicant Tracking System) score between 0 and 100, where a higher score indicates a better match.
    Provide suggestions on how the resume can be improved to better match the job description.
    
    Please return the ATS score and the feedback in the following format:
    - ATS Score: [score]
    - Suggestions for improvement: [suggestions]
    '''
    
    # Generate the response from Google Generative AI
    response = model.generate_content(prompt)
    return response.text

# Streamlit App UI
st.title("Resume Analyzer")
st.subheader("Upload your resume and job description")

# Upload the resume
uploaded_resume = st.file_uploader("Upload your resume (PDF)", type="pdf")
# Input the job description
job_description = st.text_area("Enter the job description")

# Analyze button
if st.button("Analyze"):
    if uploaded_resume is not None and job_description:
        # Read resume from the uploaded file
        resume_text = read_pdf(uploaded_resume)
        # Get the analysis result
        result = read_analyse(resume_text, job_description)
        # Display the result
        st.markdown(result)
    else:
        st.write("Please upload your resume and provide a job description.")

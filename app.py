import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

genai.configure(api_key=os.environ['GEMINI_API'])

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
    ## convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                'mime_type':'image/jpeg',
                'data' : base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    
    else:
        raise FileNotFoundError("No file uploaded")
    
# Streamlit App

st.set_page_config(page_title='JobFit Analyser')
st.header('ATS Tracking System')
input_text = st.text_area("Job Description: ", key='input')
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=['pdf'])

if uploaded_file is not None:
    st.write("PDF uploaded successfully")
    
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How can I improve my Skills")
submit3 = st.button("What are the Keywords that are Missing")
submit4 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
Provide advice and strategies for personal and professional skill development. 
Include tips on identifying areas for improvement, setting goals, creating a learning plan, seeking feedback, utilizing resources like online courses or mentorship, and staying motivated. 
Additionally, touch upon the importance of continuous learning in various aspects of life.
"""

input_prompt3 ="""
Generate a list of keywords that are missing from the given text. The text provided is [insert text here]. 
Identify and list the keywords that would enhance the content, improve searchability, or provide a more comprehensive understanding of the topic. 
Explain why each suggested keyword is relevant and briefly describe its significance in the context of the provided text.
"""

input_prompt4 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.write('Please upload the resume')
        
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.write('Please upload the resume')
        
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.write('Please upload the resume')
        
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)
        st.subheader('The Response is')
        st.write(response)
    else:
        st.write('Please upload the resume')
    
    




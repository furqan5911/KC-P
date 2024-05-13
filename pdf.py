from PyPDF2 import PdfReader
import streamlit as st
from  docx import Document
import google.generativeai as genai

# Function to generate a modification prompt and get response from generative model
def generate_prompt_and_get_response(resume_text, job_category, api_key):
    genai.configure(api_key=api_key)
    
    temperature = 0.9
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 1,
        "max_output_tokens": 99998,
    }
    
    prompt = f"Modify the following resume to better fit the job category '{job_category}':\n\n{resume_text}\n\nTry to format the response in a way that is suitable for a Word document."
    response = get_response(prompt, generation_config)
    return response

# Function to create a Word document with response text
def create_word_document(response_text):
    doc = Document()
    doc.add_paragraph(response_text)
    doc.save('modification_prompt.docx')

def get_response(prompt, generation_config, model="gemini-pro"):
    model = genai.GenerativeModel(model)
    res = model.generate_content(prompt, generation_config=generation_config)
    return res.text

def main():
    st.title("Interactive Resume Modifier")

    def extract_text_from_pdf(file):
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    if uploaded_file is not None:
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text from Resume", resume_text, height=150)
        except Exception as e:
            st.error("Please upload a valid PDF file.")
            print(e)
            st.error("Please upload a valid PDF file.")

    # Job category input
    job_categories = [
        "Software Developer", "System Analyst", "IT Project Manager", "Network Engineer",
        "Database Administrator", "Cybersecurity Specialist", "Data Scientist", "AI Engineer",
        "DevOps Engineer", "Product Manager", "UI/UX Designer", "Technical Support"
    ]
    job_category = st.selectbox("Select Job Category", job_categories)
    
    api_key = st.text_input("Enter your API key")
    
    if st.button("Generate Modification Prompt"):
        # Generate modification prompt and get response
        if uploaded_file and 'resume_text' in locals():
            # Pass extracted text as prompt
            response_text = generate_prompt_and_get_response(resume_text, job_category, api_key)
            st.text_area("Modification Prompt", response_text, height=150)
            
            # Create Word document with response text
            create_word_document(response_text)
            
            st.success("Modification prompt has been generated and saved as a Word file.")
        else:
            st.error("Please upload a resume and extract the text to generate a prompt.")

if __name__ == "__main__":
    main()

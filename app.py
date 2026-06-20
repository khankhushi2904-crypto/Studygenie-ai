import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from utils.pdf_reader import extract_text_from_pdf
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="StudyGenie AI",
    page_icon="📚"
)

st.title("📚 StudyGenie AI")
st.subheader("Your Personal AI Tutor")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.success("PDF uploaded successfully!")
    

    st.write("File Name:", uploaded_file.name)
    st.write("File Size:", round(uploaded_file.size / 1024, 2), "KB")
    if pdf_text:
     if st.button("Summarize PDF"):
        summary_prompt = f"""
        Summarize the following PDF in simple points:

        {pdf_text}
        """

        with st.spinner("Generating Summary..."):
         summary = model.generate_content(summary_prompt)
        st.subheader("PDF Summary")
        st.write(summary.text)
        st.download_button(
    "Download Summary",
    summary.text,
    file_name="summary.txt"
)
if st.button("Generate Important Questions"):

    important_prompt = f"""
    Generate 10 important exam questions from the following PDF.

    PDF Content:
    {pdf_text}
    """

    with st.spinner("Generating Important Questions..."):
        important_questions = model.generate_content(important_prompt)

    st.subheader("Important Questions")
    st.write(important_questions.text)   
if st.button("Generate Flashcards"):

    flashcard_prompt = f"""
    Create 10 flashcards from the following PDF.

    Format:
    Q: Question
    A: Answer

    PDF Content:
    {pdf_text}
    """

    with st.spinner("Generating Flashcards..."):
        flashcards = model.generate_content(flashcard_prompt)

    st.subheader("Flashcards")
    st.write(flashcards.text)
# Flashcards wala code khatam

if st.button("Generate MCQs"):

    mcq_prompt = f"""
    Create 10 multiple choice questions from the following PDF.

    Format:

    Question:
    A)
    B)
    C)
    D)

    Correct Answer:

    PDF Content:
    {pdf_text}
    """

    with st.spinner("Generating MCQs..."):
        mcqs = model.generate_content(mcq_prompt)

    st.subheader("MCQs")
    st.write(mcqs.text)

     
question = st.text_input("Ask AI anything")

if st.button("Ask AI"):
    if question:

        if pdf_text:
            prompt = f"""
            PDF Content:
            {pdf_text}

            Question:
            {question}

            Answer based only on the PDF content.
            """

            response = model.generate_content(prompt)

        else:
            response = model.generate_content(question)

        st.write(response.text)
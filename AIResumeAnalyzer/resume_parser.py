from pypdf import PdfReader
from docx import Document

def extract_text_from_pdf(file):
    text = ""

    reader = PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def extract_text_from_docx(file):
    text = ""

    document = Document(file)

    for paragraph in document.paragraphs:
        if paragraph.text:
            text += paragraph.text + "\n"

    return text

def extract_resume_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    else:
        raise ValueError("Please upload a PDF or DOCX file.")
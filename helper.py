from docx import Document
import PyPDF2

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = [paragraph.text for paragraph in doc.paragraphs]
    full_text = '\n'.join(text)
    return full_text[full_text.find('Write your answer')+len('Write your answer'):]

def extract_text_from_pdf(pdf_file):
    full_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        full_text += page.extract_text()
    return full_text[full_text.find('Write your answer')+len('Write your answer'):]
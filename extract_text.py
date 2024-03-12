import datetime
import PyPDF2
import docx

def extract_text_pdf(file):
    full_text = ''
    pdf_reader = PyPDF2.PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        full_text += page.extract_text()
    return full_text[full_text.find('Write your answer')+len('Write your answer'):]

def extract_text_docx(file):
    full_text = ''
    doc = docx.Document(file)
    for paragraph in doc.paragraphs:
        full_text += paragraph.text
    return full_text[full_text.find('Write your answer')+len('Write your answer'):]

def extract_text(file, file_type):
    if file_type == 'application/pdf':
        return extract_text_pdf(file)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_docx(file)
    else:
        return ''
    
def update_textAssignments(files):
    listTextAssignments = []
    for file in files:
        file_name = file.filename
        file_type = file.content_type
        file_text = extract_text(file, file_type)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_info = {
            'timestamp': timestamp,
            'file_name': file_name,
            'file_text': file_text
        }
        listTextAssignments.append(file_info)
    print('usando funcion update_textAssignments', listTextAssignments)
    return listTextAssignments
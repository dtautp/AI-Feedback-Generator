from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def document_print(dic_list, output_path,output_file_name):
    doc = Document()
    for item in dic_list:
        for key, value in item.items():
            text = str(value[1])
            if(value[0]==2):
                doc.add_heading(text, level=1)
            else:
                if(value[0]==0):
                    text = text
                elif(value[0]==1):
                    text = '\n' + text
                key_paragraph = doc.add_paragraph()
                key_run = key_paragraph.add_run(f"{key}: ")
                key_run.bold = True
                value_run = key_paragraph.add_run(text)
                value_run.bold = False
        doc.add_paragraph()
    doc.save(output_path + output_file_name)
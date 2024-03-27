from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import json
import time
import io

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
    # doc.save(output_path + output_file_name)
    f = io.BytesIO()
    doc.save(f)
    f.seek(0)
    return f
    # return output_path + output_file_name


def preparar_diccionario(request_list):
    dic_lis = []
    for request_key in request_list.keys():
        request = request_list[request_key]
        dic = {}
        dic['archivo_nombre'] = (2, request['file_name'])
        dic['Fecha proceso'] = (0, request['time_stamp'])
        dic['Tarea entregada'] = (1, request['user_prompt'])
        text = ''
        print(request['result_text'])
        try:
            text += json.loads(request['result_text'])['first_paragraph'] + '\n\n'
        except Exception:
            text += 'Error Formato - 1er Parrafo\n\n'
            print(Exception)
        try:
            for j in json.loads(request['result_text'])['second_paragraph']:
                text += j[list(j.keys())[0]] + ' '
        except Exception:
            text += 'Error Formato - 2do Parrafo '
            print(Exception)
        
        dic['Feedback'] = (1, text)
        dic_lis.append(dic)

    file_name = document_print(dic_lis, './temp_files/',str(int(time.time()*1000))+'.docx')


    return file_name
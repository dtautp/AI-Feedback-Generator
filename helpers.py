from datetime import datetime, timedelta
import uuid
import json
import re

def email_to_code(email):
    user_id = email.split('@')[0]
    return user_id

def generate_id():
    return str(uuid.uuid4())

def get_datetime():
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return fecha_actual

def time_stamp():
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_date

def format_datetime(datetime_default):
    datetime_format = datetime.strptime(datetime_default, '%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
    return datetime_format.strftime('%d/%m/%Y %I:%M %p')

def format_time_stamp(datetime_default):
    datetime_format = datetime.strptime(datetime_default, "%d/%m/%Y %H:%M:%S") - timedelta(hours=5)
    return datetime_format.strftime('%d/%m/%Y %I:%M %p')    

def first_paragraph_value(result_text):
    first_paragraph_match = re.search(r'"first_paragraph" : "(.*?)",', result_text)
    if first_paragraph_match:
        first_paragraph = first_paragraph_match.group(1)
    else:
        first_paragraph = None
    return first_paragraph

    
def second_paragraph_value(result_text):
    start_index = result_text.find('"second_paragraph"') + len('"second_paragraph"') + 1
    end_index = result_text.find("]", start_index)

    # Extraer el texto de "second_paragraph"
    second_paragraph_text = result_text[start_index:end_index]

    # Encontrar todas las coincidencias de ideas
    ideas = []
    index = 0
    while True:
        idea_key = f'"idea_{index+1}"'
        start_index = second_paragraph_text.find(idea_key)
        if start_index == -1:
            break
        start_index += len(idea_key) + 3
        end_index = second_paragraph_text.find('"', start_index)
        ideas.append(second_paragraph_text[start_index-1:end_index])
        index += 1

    concatenated_ideas = ' '.join(ideas)
    return concatenated_ideas
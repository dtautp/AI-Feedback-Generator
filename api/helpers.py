from datetime import datetime, timedelta
import uuid
import json
import re

def email_to_code(email):
    user_id = email.split('@')[0]
    return user_id.lower()

def generate_id():
    return str(uuid.uuid4())

def get_datetime():
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return fecha_actual

def time_stamp():
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_date

def format_datetime(datetime_default):
    datetime_format = datetime.strptime(datetime_default, '%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
    return datetime_format.strftime('%d/%m/%Y %I:%M %p')

def format_time_stamp(datetime_default):
    datetime_format = datetime.strptime(datetime_default, "%d/%m/%Y %H:%M:%S") - timedelta(hours=5)
    return datetime_format.strftime('%d/%m/%Y')    

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

def get_form_by_homework(homework_number):
    homework_form = {
        'S04' : 'no form',
        'S07' : 'https://docs.google.com/forms/d/e/1FAIpQLScmrgxoztCG0sXEi0BPVCLwYaYT6yFGd7HB-6lv2ttv6cvLAw/viewform?usp=pp_url&entry.611754790=',
        'S09' : 'https://docs.google.com/forms/d/e/1FAIpQLSdA2thYoQSwrCgsMfu0k_RPeikhOwbA9CY82RD3IZyXqIA_TA/viewform?usp=pp_url&entry.611754790=',
        'S12' : 'no form',
        'S14' : 'no form',
        'S17' : 'no form'
    }

    return homework_form.get(homework_number, "no form")

def get_feedback(result_text):
    result_json = json.loads(result_text)
    result = ''
    for i in result_json['feedback']:
        result += '- ' + i + '\n'
    result += '\n' +result_json['general-comment']
    return result

def get_feedback_print(result_text):
    try:
        result_json = json.loads(result_text)
    except Exception as e:
        print(e)
        print(result_text)
        return 'error formato'
    lis_result = []
    for i in result_json['feedback']:
        lis_result.append('- ' + i)
    lis_result.append('')
    lis_result.append(result_json['general-comment'])
    return lis_result
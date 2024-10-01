from datetime import datetime, timedelta
import uuid
import json
import re
import html

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
    # datetime_format = datetime.strptime(datetime_default, '%Y-%m-%d %H:%M:%S') - timedelta(hours=5)
    datetime_format = datetime.strptime(datetime_default, '%Y-%m-%d %H:%M:%S')
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
        'S04' : 'https://docs.google.com/forms/d/e/1FAIpQLSc2E6385BKy7Tdi-fyQIPLqG9AWI5mPKzU76jehojXNxa2Fmw/viewform?usp=pp_url&entry.611754790=',
        'S07' : 'https://docs.google.com/forms/d/e/1FAIpQLScmrgxoztCG0sXEi0BPVCLwYaYT6yFGd7HB-6lv2ttv6cvLAw/viewform?usp=pp_url&entry.611754790=',
        'S09' : 'https://docs.google.com/forms/d/e/1FAIpQLSdA2thYoQSwrCgsMfu0k_RPeikhOwbA9CY82RD3IZyXqIA_TA/viewform?usp=pp_url&entry.611754790=',
        'S12' : 'https://docs.google.com/forms/d/e/1FAIpQLSeR07pEJXEy5WCre_5kOwY3IIaSbz_vFxXEJNyVhPb4BVkuOA/viewform?usp=pp_url&entry.611754790=',
        'S14' : 'https://docs.google.com/forms/d/e/1FAIpQLSfFuZ5MHaCdq5k4PmA5JW1PZdOu6lNrtloYrgQgIcyA-p6oGw/viewform?usp=pp_url&entry.611754790=',
        'S17' : 'https://docs.google.com/forms/d/e/1FAIpQLSchfWTIpidsQQ4s-xOM3mRezdj0d77aFcc2eUgCf_jQ7mqIjg/viewform?usp=pp_url&entry.611754790='
    }

    return homework_form.get(homework_number, "no form")

def get_feedback(result_text):
    result_json = json.loads(result_text)
    result = ''
    for i in result_json['feedback']:
        result +=  i + '\n'
    result += '\n' +result_json['general-comment']
    return result

def get_name_homework(homework_number):
    homework_form = {
        'S04' : '🔴 (AC-S04) Week 04 - Task: Assignment – Jobs and Occupation',
        'S07' : '🔴 (AC-S07) Week 07 - Task: Assignment - My Family',
        'S09' : '🔴 (AC-S09) Week 09 - Task: Assignment - A family member I admire',
        'S12' : '🔴 (AC-S12) Week 12 - Task: Assignment – What\'s their daily routine?',
        'S14' : '🔴 (AC-S14) Week 14 - Task: Assignment - Things I like and don\'t like',
        'S17' : '🔴 (AC-S17) Week 17 - Task: Assignment - Final Assignment - “Applying to Disney - Part I'
    }

    return homework_form.get(homework_number, "no name")
from openai import OpenAI
import os
import time
import datetime
import json
from firebase_module import select_system_prompt_by_id

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

conversations = []

def create_post_openAI(question):
    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo-0125',
        messages= [
            {"role": "system", "content": 'Create feedback for a student\'s homework in an English class. Give feedback in a pedagogical way. Give the feedback considering that the students you are giving feedback to have entry level knowledge of the language. Give feedback as if you were a cool teacher, use emojis to make the message feel more friendly, but do NOT salute the student by its name. Give feedback ONLY about grammar AND vocabulary use, do NOT take in count capitalization mistakes. To give feedback use two paragraphs. The first paragraph should give general feedback about student performance overall, this paragraph must be present in your answer. The second paragraph should let the student know what their mistakes were and which language rules apply in those cases. This paragraph is optional, add it in your answer only if the student has made any grammar or vocabulary mistake, otherwise leave it blank. Give the second paragraph separated into ideas, each idea should talk about a specific mistake. Finally, let know in your answer the number of mistakes made by the student. To give me your answer use json format with the following structure: {"first_paragraph" : "","second_paragraph":["Idea 1", "Idea 2",...]}'},
            {"role": "user", "content" : question}
        ],
        temperature = 0.6,
        max_tokens = 1000,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )
    return str(response.choices[0].message.content)



def time_stamp():
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%d/%m/%Y %H:%M:%S")
    return formatted_date


def api_price_calculator(usage):
    COMPLETION_TOKEN_PRICE=0.0000015
    PROMPT_TOKEN_PRICE=0.0000005
    return (usage['prompt_tokens']*PROMPT_TOKEN_PRICE) + (usage['completion_tokens']*COMPLETION_TOKEN_PRICE)

def prompt_request(prompt, user_prompt, seed,temp_t, frequency_penalty):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
        "role": "system",
        "content": prompt,
        
        },  {
          "role" : "user",
          "content" : user_prompt
      }
    ],
    temperature=temp_t,
    max_tokens=500,
    # seed=seed,
    top_p=1,
    frequency_penalty=frequency_penalty,
    presence_penalty=0
    )
    return response

def request_prompt(system_prompt_id,user_prompt):
    PROMPT_ID = system_prompt_id
    system_prompt = select_system_prompt_by_id(system_prompt_id)
    PROMPT = system_prompt['prompt_content']
    TEMPERATURA = system_prompt['temperatura']
    FREQUENCY_PENALTY = system_prompt['frecuency_penalty']
    SEED = None
    time_start = time.time()
    res = prompt_request(PROMPT, user_prompt, SEED,TEMPERATURA, FREQUENCY_PENALTY)
    time_end = time.time()
    EXECUTIOM_TIME = time_end - time_start
    response_dict = json.loads(res.json())
    return_dic = {
        'system_prompt_id': PROMPT_ID,
        'user_prompt': user_prompt,
        'seed': SEED,
        'system_fingerprint': response_dict['system_fingerprint'],
        'usage': response_dict['usage'],
        'message': response_dict['choices'][0]['message']['content'],
        'time_stamp': time_stamp(),
        'price': api_price_calculator(response_dict['usage']),
        'execution_time': EXECUTIOM_TIME
    }
    return return_dic


def extract_feedback_from_response(respuesta_diccionario):
    mensaje_respuesta = json.loads(respuesta_diccionario['message'])
    try:
        feedback = 'Feedback:\n'+ mensaje_respuesta['first_paragraph'] + '\n\n'
    except:
        feedback = 'Error de formato primer parrafo'
    try:
        for i in mensaje_respuesta['second_paragraph']:
            feedback += i[list(i.keys())[0]] + '\n'
    except:
        feedback += 'Sin feedback específico'
    return feedback
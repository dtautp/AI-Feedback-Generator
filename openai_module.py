from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

conversations = []

def create_post_openAI(question):

    response = client.chat.completions.create(
        model = 'gpt-3.5-turbo-0125',
        messages= [
            {"role": "system", "content": ""},
            {"role": "user", "content" : question}
        ],
        temperature = 0.5,
        max_tokens = 150,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0.6
    )

    answer = 'AI: ' + str(response.choices[0].message.content)
    question = 'Yo: ' + question

    conversations.append(question)
    conversations.append(answer)
    
    return conversations
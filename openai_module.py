from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

conversations = []

def create_post_openAI(question):

    # response = client.chat.completions.create(
    #     model = 'gpt-3.5-turbo-0125',
    #     messages= [
    #         {"role": "system", "content": ""},
    #         {"role": "user", "content" : question}
    #     ],
    #     temperature = 0.5,
    #     max_tokens = 150,
    #     top_p = 1,
    #     frequency_penalty = 0,
    #     presence_penalty = 0.6
    # )

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

    answer = 'AI: ' + str(response.choices[0].message.content)
    question = 'Yo: ' + question

    conversations.append(question)
    conversations.append(answer)
    
    return conversations
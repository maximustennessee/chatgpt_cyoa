####################
# Details
# This is a history aware choose your own adventure game
# The game chats with 

from openai import OpenAI
from dotenv import load_dotenv
import chat_messages

# load the API Key and initialize the OpenAI client
load_dotenv()
client = OpenAI()

# initialize the app-specific variables
chat_history, choice = "", ""
endings = ["goodbye, traveler", "goodbye traveler", "congratulations traveler", "congratulations, traveler"]

# continue chat loop until we encounter an exit string
while True:

    # define our interface for chatting with OpenAI
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": chat_messages.system_message.format(chat_history = chat_history)},
        {"role": "user", "content": choice}
    ]
    )

    # send the chat message and retrieve response
    response_content = completion.choices[0].message.content

    print(response_content)

    # exit the program if we encounter an exit string
    for e in endings:
        if e in response_content.lower():
            exit()

    choice = input("Your answer:")

    chat_history += chat_messages.response_message.format(response_content, choice)
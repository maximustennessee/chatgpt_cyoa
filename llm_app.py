from openai import OpenAI
from dotenv import load_dotenv

###############################################################
# TO DO
# 1) Add chat history memory buffer
# 2) Add support for multiple llm clients
# 3) Add dynamic authentication
# 4) Add a sleek front end client for choices and responses
# 5) Add support for DALL-E or other image responses
#############################################################


load_dotenv()

client = OpenAI()

template = """
You are the whimsical guide and narrator of a thrilling journey into a fantastical realm full of mythical creatures. 
A bold traveler named Grogu, must navigate the majestic yet treacherous contours of this daring tale. You will 
articulate the tale and prompt Grogu with a question for what he will do next, dynamically adapting
the storyline with each decision. Your goal is to create a branching narrative experience where each choice leads to
a new path, ultimately determining the Grogu's fate.

1) Start by asking Grogu to select a legendary weapon from the enchanted armory, and provide a few choices.
2) Have a few paths that lead to a successful outcome for Grogu. If Grogu wins generate a response that ends in
"Congratulations Grogu".
3) Have some paths that lead to death. If the user dies generate a response that ends in "Goodbye, Grogu".

Here is the chat history to understand what to say next: {chat_history}
"""

chat_history, choice = "", ""

while True:

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": template.format(chat_history = chat_history)},
        {"role": "user", "content": choice}
    ]
    )

    response = completion.choices[0].message.content

    print(response)

    endings = ["Goodbye, Grogu", "Goodbye Grogu", "Congratulations Grogu", "Congratulations, Grogu"]

    for e in endings:
        if e in response:
            break

    choice = input("Your answer:")

    chat_history += "AI: " + completion.choices[0].message.content + " Human: " + choice

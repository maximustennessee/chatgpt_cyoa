import streamlit as st
import tools
from dotenv import load_dotenv
import chat_messages
from langchain_core.messages import HumanMessage, AIMessage

legendary_weapons = "https://www.dndbeyond.com/magic-items?filter-type=0&filter-type=9&filter-search=&filter-rarity=5&filter-requires-attunement=&filter-effect-type=&filter-effect-subtype=&filter-has-charges=&filter-partnered-content=f"

agent = tools.Agent(legendary_weapons)

chat_history = []

with st.chat_message("AI") as ai_message:
    st.write("Welcome traveler, I am Xam the dungeon master. In order to start your noble quest, choose from the available inventory:")
    response = agent.executor({"input": "what items are in my inventory? just weapon names and be exhaustive"})
    st.write(response.get("output"))

while True:
    human_message = st.chat_input("Type your message here...")
    if human_message:

        with st.chat_message("Human"):
            st.write(human_message)

        from langchain_core.messages import HumanMessage, AIMessage

        chat_history = [
            HumanMessage(content=human_message),
            AIMessage(content=ai_message)
        ]
        
        with st.chat_message("AI") as ai_message:
            st.write("hi")



import streamlit as st
import tools
from dotenv import load_dotenv
import chat_messages
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

def get_response(user_query):
    response = st.session_state.agent.executor(
        {"system": chat_messages.system_message,
         "chat_history": st.session_state.chat_history,
         "input": user_query
         })
    
    return response.get("output")

legendary_weapons = "http://localhost:8000/"

if "chat_history" not in st.session_state:
    agent = tools.Agent(legendary_weapons) 
    st.session_state.chat_history = []
    init_message = "Welcome traveler, I am Xam the dungeon master. In order to start your noble quest, choose from the available inventory. "
    response = agent.executor(
        {"input": "List the just the weapons and descriptions found in the inventory.",
         "system": chat_messages.system_message
         })
    init_message = init_message + response.get("output")
    st.session_state.chat_history.append(SystemMessage(content=chat_messages.system_message))
    st.session_state.chat_history.append(AIMessage(content=init_message))
    st.session_state.agent = agent

#sidebar
with st.sidebar:
    st.header("Chat history")

#user input
human_message = st.chat_input("Type your message here...")
if human_message:
    response = get_response(human_message)
    st.session_state.chat_history.append(HumanMessage(content=human_message))
    st.session_state.chat_history.append(AIMessage(content=response))

for m in st.session_state.chat_history:
    if isinstance(m, AIMessage):
        with st.chat_message("AI"):
            st.write(m.content)
    if isinstance(m, HumanMessage):
        with st.chat_message("Human"):
            st.write(m.content)

with st.sidebar:
    st.write(st.session_state.chat_history)

print('lower')
print(type(st.session_state.chat_history[-1].content.lower()))

for e in ["congratulations", "goodbye"]:
    if e in st.session_state.chat_history[-1].content.lower():
        # this should restart the game
        pass
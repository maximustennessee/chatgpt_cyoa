import streamlit as st
import backend
from dotenv import load_dotenv
import chat_messages

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI

tools = [TavilySearchResults(max_results=10)]

prompt = hub.pull("hwchase17/openai-tools-agent")

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)


st.set_page_config(page_title="Choose Your Own Adventure", page_icon="🔮")

st.title("Chat with websites")

client = OpenAI()
ai_message = """Welcome traveler, I am Xam the dungeon master. 
                In order to start your noble quest, choose from the available inventory: {inv}
                """.format(inv=backend.inventory_raw)

prompt = ChatPromptTemplate.from_messages([
    ("system", chat_messages.system_message),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

with st.chat_message("AI") as ai_message:
    st.write("Welcome traveler, I am Xam the dungeon master. In order to start your noble quest, choose from the available inventory:")
    for i in backend.inventory_raw:
        st.write(i)

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
            st.write(completion.choices[0].message.content)



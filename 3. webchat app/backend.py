from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import chat_messages

load_dotenv()
llm = ChatOpenAI()

# Load the inventory
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader('https://www.dndbeyond.com/equipment?filter-search=Weapon')
inventory = loader.load()

# Initialize vectorstore using inventory
from langchain_openai import OpenAIEmbeddings

# Use OpenAI embedding to measure relatedness of strings
embeddings = OpenAIEmbeddings()

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(inventory)

vectorstore = FAISS.from_documents(documents, embeddings)

# Create chain for passing list of documents to model
from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template(chat_messages.chat_prompt_template)
document_chain = create_stuff_documents_chain(llm, prompt)

from langchain.chains import create_retrieval_chain

vectorstore_retriever = vectorstore.as_retriever()
retrieval_chain = create_retrieval_chain(vectorstore_retriever, document_chain)

response = retrieval_chain.invoke({
    "input" : "List the names of all the available weapons."
})

# We'll use this later
ai_message = response.get('answer')

from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
])

retriever_chain = create_history_aware_retriever(llm, vectorstore_retriever, prompt)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the users questions based on the below contenxt:\n\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

document_chain = create_stuff_documents_chain(llm, prompt)

conversation_retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

from langchain_core.messages import HumanMessage, AIMessage

chat_history = [
    HumanMessage(content="List the names of all the available weapons in the following the format: 1. Weapon 1\n2. Weapon 2."),
    AIMessage(content=ai_message)
]
response = conversation_retrieval_chain.invoke({
    "chat_history": chat_history,
    "input": "List the names of all the ranged weapons, and their weights, in following the format: 1. Weapon 1, (WEIGHT)\n2. Weapon 2 (WEIGHT). If no weight is available use '2 lbs'"
})

inventory_raw = response.get('answer').split('\n')
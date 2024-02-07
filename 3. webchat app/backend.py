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

retriever = vectorstore.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({
    "input" : "List the names of all the available weapons."
})

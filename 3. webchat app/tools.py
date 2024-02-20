#!/usr/bin/env python
from typing import List
from dotenv import load_dotenv

# from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
# from langserve import add_routes
load_dotenv()

class Agent():

    def __init__(self, url):
        loader = WebBaseLoader(url)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        embeddings = OpenAIEmbeddings()
        self.vector = FAISS.from_documents(documents, embeddings)
        self.retriever = self.vector.as_retriever()
        self.retriever_tool = create_retriever_tool(
            self.retriever,
            "inventory_search",
            "For any questions about inventory you must use this tool.",
        )
        self.search = TavilySearchResults()
        self.tools = [self.retriever_tool, self.search]
        self.prompt = hub.pull("hwchase17/openai-functions-agent")
        # Keep temperature at 0 or risk insanity
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.agent = create_openai_functions_agent(self.llm, self.tools, self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

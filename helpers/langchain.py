import os
from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Pinecone
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.agents.types import AgentType
from langchain.schema import HumanMessage, AIMessage


from app.partner.model import Partner

def qa_chain(question, history=[], partner: Partner = Partner(), doc_store='pinecone'):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    if doc_store == 'pinecone':
        pinecone.init(
            api_key=os.getenv('PINECONE_API_KEY'),
            environment=os.getenv('PINECONE_API_ENV'),
        )

        docsearch = Pinecone.from_existing_index(index_name=partner.identity, embedding=embeddings)
    else:
        docsearch = PGVector(
            collection_name=partner.identity,
            connection_string=os.getenv('DATABASE_URI'),
            embedding_function=embeddings,
            )
    
    llm = ChatOpenAI()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
    )

    system_message = f"""
            "You are a helpful customer support agent."
            "You provide assistant to callers about {partner.name}"
            "You can ask questions to help you understand and diagnose the problem."
            "If you are unsure of how to help, you can suggest the client to go to the nearest {partner.name} office."
            "Try to sound as human as possible"
            "Make your responses as concise as possible"
            """
    tools = [
        Tool(
            name=f"{partner.name} assistant",
            func=qa.run,
            description=f"Useful when you need to answer {partner.name} questions",
        )
    ]
    executor = initialize_agent(
        agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        # memory=conversational_memory,
        handle_parsing_errors="Check your output and make sure it conforms!",
        agent_kwargs={"system_message": system_message},
        verbose=True,
    )

    q = {"question": question}

    chat_history = []
    for h in history:
        chat_history.append(HumanMessage(content=h.question))
        chat_history.append(AIMessage(content=h.answer))

    return executor.run(input=q, chat_history=chat_history)

def pinecone_train_with_resource(resource_url, partner_identity):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_API_ENV'),
    )
    
    if partner_identity not in pinecone.list_indexes():
        # we create a new index
        pinecone.create_index(
        name=partner_identity,
        metric='cosine',
        dimension=1536
        )

    Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=partner_identity)

def pinecone_delete_resource(resource_url, partner_identity):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_API_ENV'),
    )

    index = Pinecone.get_pinecone_index(partner_identity)
    for text in texts:
        index.delete(filter={'text':{"$eq": text.page_content}})

def postgres_train_with_resource(resource_url, partner_identity):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

    PGVector.from_documents(
        embedding=embeddings,
        documents=texts,
        collection_name=partner_identity,
        connection_string=os.getenv('DATABASE_URI'),
        )
    
def train_with_resource(resource_url, partner_identity, doc_store='pinecone'):
    if doc_store == 'pinecone':
        return pinecone_train_with_resource(resource_url, partner_identity)
    return postgres_train_with_resource(resource_url, partner_identity)

def delete_resource(resource_url, partner_identity, doc_store='pinecone'):
    if doc_store == 'pinecone':
        return pinecone_delete_resource(resource_url, partner_identity)
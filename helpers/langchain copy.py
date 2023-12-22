# OLD 1

# import os
# from langchain.document_loaders import OnlinePDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.vectorstores import Pinecone
# from langchain.vectorstores.pgvector import PGVector
# from langchain.embeddings.openai import OpenAIEmbeddings

# import pinecone

# from langchain.llms import OpenAI
# from langchain.chains import ConversationalRetrievalChain
# from langchain.chains import RetrievalQA
# from langchain.prompts import SystemMessagePromptTemplate
# from langchain.prompts.chat import ChatPromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain.tools import Tool
# from langchain.agents import initialize_agent
# from langchain.agents.types import AgentType
# from langchain.schema import HumanMessage, AIMessage


# from app.partner.model import Partner

# def qa_chain(question, history=[], partner: Partner = Partner(), doc_store='postgres'):
#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

#     if doc_store == 'pinecone':
#         pinecone.init(
#             api_key=os.getenv('PINECONE_API_KEY'),
#             environment=os.getenv('PINECONE_API_ENV'),
#         )

#         docsearch = Pinecone.from_existing_index(index_name=partner.identity, embedding=embeddings)
#     else:
#         docsearch = PGVector(
#             collection_name=partner.identity,
#             connection_string=os.getenv('DATABASE_URI'),
#             embedding_function=embeddings,
#             )
    
#     llm = ChatOpenAI()
#     qa = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=docsearch.as_retriever(),
#     )

#     system_message = f"""
#             "You are a helpful customer support agent."
#             "You provide assistant to callers about {partner.name}"
#             "You can ask questions to help you understand and diagnose the problem."
#             "If you are unsure of how to help, you can suggest the client to go to the nearest {partner.name} office."
#             "Try to sound as human as possible"
#             "Make your responses as concise as possible"
#             """
#     tools = [
#         Tool(
#             name=f"{partner.name} assistant",
#             func=qa.run,
#             description=f"Useful when you need to answer {partner.name} questions",
#         )
#     ]
#     executor = initialize_agent(
#         agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
#         tools=tools,
#         llm=llm,
#         # memory=conversational_memory,
#         handle_parsing_errors="Check your output and make sure it conforms!",
#         agent_kwargs={"system_message": system_message},
#         verbose=True,
#     )

#     q = {"question": question}

#     chat_history = []
#     for h in history:
#         chat_history.append(HumanMessage(content=h.question))
#         chat_history.append(AIMessage(content=h.answer))

#     return executor.run(input=q, chat_history=chat_history)

#     # OLD 2
#     # general_system_template = f"""
#     #         "You are a helpful customer care assistant."
#     #         "You provide assistant to callers about {partner.name}"
#     #         "You can ask questions to help you understand and diagnose the problem."
#     #         "If you are unsure of how to help, you can suggest the client to go to the nearest {partner.name} office."
#     #         "Try to sound as human as possible"
#     #         "Your responses are always as short as possible"
#     #         "Based on the following context, provide a final answer:"
#     #         {{context}}
#     #         "Additional information: Please note that if the context does not have the answer to the question, you can ask further question to better understand the customer problem."
#     #         """
#     # messages = [
#     #     SystemMessagePromptTemplate.from_template(general_system_template),
#     #     ]
    
#     # qa_prompt = ChatPromptTemplate.from_messages( messages )

#     # qa = ConversationalRetrievalChain.from_llm(
#     #     llm=ChatOpenAI(temperature=0),
#     #     retriever=docsearch.as_retriever(),
#     #     chain_type="stuff",
#     #     # verbose=True,
#     #     combine_docs_chain_kwargs={'prompt': qa_prompt}
#     #     )

#     # result = qa({"question": question, "chat_history": [(h.question, h.answer) for h in history]})

#     # return result["answer"]

#     # OLD 1
#     # qa = ConversationalRetrievalChain.from_llm(
#     #     OpenAI(temperature=0), docsearch.as_retriever()
#     #     )

#     # result = qa({"question": question, "chat_history": [(h.question, h.answer) for h in history]})

#     # return result["answer"]

# def pinecone_train_with_resource(resource_url, partner_identity):
#     loader = OnlinePDFLoader(resource_url)

#     data = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_documents(data)
    

#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

#     pinecone.init(
#         api_key=os.getenv('PINECONE_API_KEY'),
#         environment=os.getenv('PINECONE_API_ENV'),
#     )
    
#     if partner_identity not in pinecone.list_indexes():
#         # we create a new index
#         pinecone.create_index(
#         name=partner_identity,
#         metric='cosine',
#         dimension=1536
#         )

#     Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=partner_identity)

# def postgres_train_with_resource(resource_url, partner_identity):
#     loader = OnlinePDFLoader(resource_url)

#     data = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     texts = text_splitter.split_documents(data)
    

#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

#     PGVector.from_documents(
#         embedding=embeddings,
#         documents=texts,
#         collection_name=partner_identity,
#         connection_string=os.getenv('DATABASE_URI'),
#         )
    
# def train_with_resource(resource_url, partner_identity, doc_store='postgres'):
#     if doc_store == 'pinecone':
#         return pinecone_train_with_resource(resource_url, partner_identity)
#     return postgres_train_with_resource(resource_url, partner_identity)

# OLD 2

import os
from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Pinecone
from langchain.vectorstores.pgvector import PGVector
from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone

from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain.prompts import SystemMessagePromptTemplate
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.agents.types import AgentType
from langchain.schema import HumanMessage, AIMessage


from app.partner.model import Partner

def qa_chain(question, history=[], partner: Partner = Partner(), doc_store='postgres'):
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

    # OLD 2
    # general_system_template = f"""
    #         "You are a helpful customer care assistant."
    #         "You provide assistant to callers about {partner.name}"
    #         "You can ask questions to help you understand and diagnose the problem."
    #         "If you are unsure of how to help, you can suggest the client to go to the nearest {partner.name} office."
    #         "Try to sound as human as possible"
    #         "Your responses are always as short as possible"
    #         "Based on the following context, provide a final answer:"
    #         {{context}}
    #         "Additional information: Please note that if the context does not have the answer to the question, you can ask further question to better understand the customer problem."
    #         """
    # messages = [
    #     SystemMessagePromptTemplate.from_template(general_system_template),
    #     ]
    
    # qa_prompt = ChatPromptTemplate.from_messages( messages )

    # qa = ConversationalRetrievalChain.from_llm(
    #     llm=ChatOpenAI(temperature=0),
    #     retriever=docsearch.as_retriever(),
    #     chain_type="stuff",
    #     # verbose=True,
    #     combine_docs_chain_kwargs={'prompt': qa_prompt}
    #     )

    # result = qa({"question": question, "chat_history": [(h.question, h.answer) for h in history]})

    # return result["answer"]

    # OLD 1
    # qa = ConversationalRetrievalChain.from_llm(
    #     OpenAI(temperature=0), docsearch.as_retriever()
    #     )

    # result = qa({"question": question, "chat_history": [(h.question, h.answer) for h in history]})

    # return result["answer"]

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
    
def train_with_resource(resource_url, partner_identity, doc_store='postgres'):
    if doc_store == 'pinecone':
        return pinecone_train_with_resource(resource_url, partner_identity)
    return postgres_train_with_resource(resource_url, partner_identity)
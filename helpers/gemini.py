import os

import google.generativeai as genai

from app.partner.model import Partner

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)


# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import pinecone
from langchain.vectorstores.pinecone import Pinecone
# from langchain.schema.output_parser import StrOutputParser
# from langchain.schema.runnable import RunnableMap
# from langchain.prompts import ChatPromptTemplate

from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


# llm = ChatGoogleGenerativeAI(model="gemini-pro",
#                              temperature=0.7)

# def dotest():
#     result = llm.invoke("What is a LLM?")
#     print(result.content)

def qa_chain(question = "What happened to the oceangate submersible?", history=[], partner: Partner = Partner()):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_API_ENV'),
    )

    docsearch = Pinecone.from_existing_index(index_name=partner.identity, embedding=embeddings)
    retriever=docsearch.as_retriever()

    system_message = f"""
            "You are a helpful customer support agent."
            "You provide assistant to callers about {partner.name}"
            "You can ask questions to help you understand and diagnose the problem."
            "If you are unsure of how to help, you can suggest the client to go to the nearest {partner.name} office."
            "Try to sound as human as possible"
            "Make your responses as concise as possible"
            "Your response must be in plain text"
            """

    model = genai.GenerativeModel('gemini-pro')

    messages = [
        {
            'role':'user',
            'parts': [system_message]
            }
    ]
    for h in history:
        messages[0]['parts'].append(h.question)
        messages[0]['parts'].append(h.answer)
    
    retrieved = retriever.get_relevant_documents(question)
    context = "\n".join([document.page_content for document in retrieved])

    messages[0]['parts'].append(f"Based on our conversation and the context below: {question}\n Context: {context}")
    
    response = model.generate_content(messages)
    return response.text

def pinecone_train_with_resource(resource_url, partner_identity):
    loader = OnlinePDFLoader(resource_url)

    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

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

# def qa_chain(question = "What happened to the oceangate submersible?", history=[], partner: Partner = Partner()):
#     embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     pinecone.init(
#         api_key=os.getenv('PINECONE_API_KEY'),
#         environment=os.getenv('PINECONE_API_ENV'),
#     )

#     docsearch = Pinecone.from_existing_index(index_name=partner.identity, embedding=embeddings)
#     retriever=docsearch.as_retriever()

#     template = """Answer the question a a full sentence, based only on the following context:
#     {context}

#     Question: {question}
#     """
#     prompt = ChatPromptTemplate.from_template(template)

#     # system_message = f"""
#     #         "You are a helpful customer support agent."
#     #         "You provide assistant to callers about {partner.name}"
#     #         "You can ask questions to help you understand and diagnose the problem."
#     #         "If you are unsure of how to help, you can suggest the client to go to the nearest {partner.name} office."
#     #         "Try to sound as human as possible"
#     #         "Make your responses as concise as possible"
#     #         """

#     output_parser = StrOutputParser()

#     chain = RunnableMap(
#         {
#             "context": lambda x: retriever.get_relevant_documents(x[-1]),
#             "question": lambda x: x[-1]
#             }) | prompt | llm | output_parser

#     messages = []
#     for h in history:
#         messages.append(HumanMessage(content=h.question))
#         messages.append(AIMessage(content=h.answer))
    
#     messages.append(HumanMessage(content=question))

#     return chain.invoke([messages])
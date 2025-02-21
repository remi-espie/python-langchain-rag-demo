import sys

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, ChatOllama

def chroma_save():
    # Load the document
    with open('training.txt', 'r') as f:
        training_data = f.readlines()

    # Split the combined text into chunks
    documents = [Document(page_content=line) for line in training_data]

    # Create a vector store using Chroma DB, our chunked data from the URLs, and the nomic-embed-text embedding model
    vectorstore = Chroma.from_documents(
        documents=documents,
        collection_name="rag-chroma",
        embedding=OllamaEmbeddings(model='nomic-embed-text'),
        persist_directory="rag-chroma",
    )

    return vectorstore

def chroma_load():
    return Chroma(
        collection_name="rag-chroma",
        embedding_function=OllamaEmbeddings(model='nomic-embed-text'),
        persist_directory="rag-chroma",
    )


def process_input(question):
    model_local = ChatOllama(model="phi4", temperature=0)

    # vectorstore = chroma_save()
    vectorstore = chroma_load()
    retriever = vectorstore.as_retriever()

    # Create a question / answer pipeline
    rag_template = """You are an assistant for solving chess moves. Use the following pieces of retrieved context to answer the question. The context may not contain the answer. Only answer with the move and nothing else.
    Chess board state: {question}
    Context: {context}
    Answer:
    """
    rag_prompt = ChatPromptTemplate.from_template(rag_template)
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | model_local
        | StrOutputParser()
    )
    # Invoke the pipeline
    return rag_chain.invoke(question)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 app.py '<question>'")
        sys.exit(1)

    question = sys.argv[1]
    answer = process_input(question)
    print(answer)

import sys
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

def process_input(question):
    # Load URLs from the sources.txt file and split them at newline characters
    with open("sources.txt", "r") as file:
        urls_list = file.read().strip().split("\n")
    
    # You can use a base_url param to change the ollama instance that it uses (default is http://localhost:11434)
    # If you don't set the cache param, it won't cache anything
    # You can set a format param to json if you want it to output json
    model_local = ChatOllama(model="phi3")
    
    # Load documents from URLs
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    # This is where it "chunks" the data from the URLs
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)

    # Create a vector store using Chroma DB, our chunked data from the URLs, and the nomic-embed-text embedding model
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
    )
    retriever = vectorstore.as_retriever()

    # Create a question / answer pipeline 
    rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
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
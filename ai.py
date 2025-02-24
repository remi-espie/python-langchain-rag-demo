import sys
import pandas as pd
import re
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

def start_langchain():
    model_local = ChatOllama(model="phi3.5", temperature=0)
    df = pd.read_csv("club_games_data.csv")
    # Filter by really winned games
    filtered_df = df[(df['white_result'] == 'checkmated') | (df['black_result'] == 'checkmated')]

    # Get last line of each filtered game
    game_list = filtered_df['pgn'].apply(lambda x: x.split('\n')[-2]).tolist()
    # Remove all occurrences of `{[%clk ...]}`
    game_list = [re.sub(r'\{\[%clk[^\{]*?\]\} [0-9]+\.\.\.', '', game) for game in game_list]
    game_list = [re.sub(r'\{\[%clk.*?\]\}', '', game) for game in game_list]
    game_list = ["game: " + game for game in game_list]
    game_list = game_list[:15000]
    combined_text = "\n".join(game_list)
    with open("games.txt", "w") as f:
        f.write(combined_text)

    # Split the combined text into chunks
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_text(combined_text)
    documents = [Document(page_content=chunk) for chunk in doc_splits]


    # Create a vector store using Chroma DB, our chunked data from the URLs, and the nomic-embed-text embedding model
    vectorstore = Chroma.from_documents(
        documents=documents,
        collection_name="rag-chroma",
        embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

    return model_local, retriever

def new_move(question, model_local, retriever):
    # Create a question / answer pipeline
    rag_template = """Here are lots of different chess games represented by their moves.
    {context}
    You're playing a game right now. You're playing white. Here are the current game moves: {question}. 
    What should you play next? The move must be valid. Output only the move. Output one move between quotes. For example, "e4" or "Nf3".
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

def first_move(model_local, retriever):
    # Create a question / answer pipeline
    rag_template = """Here are lots of different chess games represented by their moves.
    {context}
    You're playing a game right now. You're playing white.  
    What move should you start with? The move must be valid. 
    Output only the move. Output one move between quotes. For example, "e4" or "Nf3".
    """
    rag_prompt = ChatPromptTemplate.from_template(rag_template)
    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | rag_prompt
            | model_local
            | StrOutputParser()
    )

    # Invoke the pipeline
    return rag_chain.invoke("")


if __name__ == "__main__":
    model_local, retriever = start_langchain()
    print("----------")
    answer = first_move(model_local, retriever)
    print(answer)
    while True:
        answer = new_move(input("Enter a command to play a move: "), model_local, retriever)
        print(answer)
# Python / LangChain / Ollama RAG Demo

This is the code that we used in [the June 28 Crafting Intelligent Python Apps with Retrieval-Augmented Generation Open Space](https://that.us/activities/5EI62c1gogbMFYMqilkP).  This is a command line interface (CLI) app but you can expand it to be a web service.  This should run on a Windows PC but these instructions assume that you are using MacOS.

## Steps to run this locally

1. [Install Ollama on your computer](https://ollama.com/download)
2. Pull down this project from [Github](https://github.com/steinbring)
3. Navigate to the project folder in [iterm2](https://iterm2.com/) (or Terminal)
4. Pull down phi3
	1. `ollama pull phi3`
5. Pull down nomic-embed-text
	1. `ollama pull nomic-embed-text`
4. Set up your Python virtual environment
	1. `pip install virtualenv` (if needed)
	2. `python3 -m venv ragdemo`
	3. `source ragdemo/bin/activate`
5. Install LangChain, beautifulsoup4, tiktoken, and Chroma DB
	1. `pip install langchain_community`
	2. `pip install beautifulsoup4`
	3. `pip install tiktoken`
	4. `pip install chromadb`
6. Run the app (making an actual query)
	1. `python3 app.py "What did apple announce?"`

## Are you having trouble running this?

Feel free to contact me on [Mastodon](https://toot.works/@joe) or [Signal](https://signal.me/#eu/wYx/v3zx0aPCt1RvLXBtCTcrKGWK0hJiIw2JpsQatK5UCSN9YMpDurXTeZ11atLj)

## Can you do this without LangChain?

Yeah, as of last month, you can.  I wrote [an article about how to do it](https://jws.news/2024/how-to-get-ai-to-tell-you-the-flavor-of-the-day-at-kopps/).

## What if I missed this Open Space?

[I am planning on presenting "The Scoop on Embedding: Teaching Large Language Models the 'Flavor of the Day' at Culvers" on August 23 at DevCon Midwest](https://events.nvisia.com/conference/be3edb0f-815e-48dd-9826-9b62f6fbc93a)

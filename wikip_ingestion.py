from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from bs4 import BeautifulSoup
import pandas as pd
from langchain_community.document_loaders import WikipediaLoader

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

INDEX_NAME = "langchain-doc-index"


def ingest_docs():
    print("ingesting docs!!")
    
    #wikiurl = 'https://en.wikipedia.org/wiki/Solar_System#:~:text=The%20inner%20Solar%20System%20includes,bodies%20in%20the%20Kuiper%20belt.'
    #tables = pd.read_html(wikiurl)
    #print(tables)



    loader = WikipediaLoader(query="Solar System")

    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)

    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(
        documents, embeddings, index_name=INDEX_NAME
    )
    
    print("****Loading to vectorstore done ***")


if __name__ == "__main__":
    ingest_docs()



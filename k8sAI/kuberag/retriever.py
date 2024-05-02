# file: k8sAI/kuberag/retriever.py

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from k8sAI.util import console


def load_retriever(embeddings_path: str):
    """
    Load a retriever from a given embeddings path.
    """
    vectordb = Chroma(
        persist_directory=embeddings_path,
        embedding_function=OpenAIEmbeddings(disallowed_special=()),
    )

    # Check if the vector database is empty and log a warning if so
    if len(vectordb.get(limit=1).get("documents", [])) == 0:
        console.print("Warning: The vector database is empty.")

    retriever = vectordb.as_retriever(
        search_type="mmr",  # Also test "similarity"
        search_kwargs={"k": 8},
    )
    return retriever

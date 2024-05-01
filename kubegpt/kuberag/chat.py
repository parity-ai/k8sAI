# file: kubegpt/kuberag/chat.py

from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")


retriever_prompt = ChatPromptTemplate.from_messages(
    [
        ("placeholder", "{chat_history}"),
        ("user", "{input}"),
        (
            "user",
            "Given the above information, generate a search query to look up to\
                  get information relevant to the conversation",
        ),
    ]
)

chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful, concise chatbot and kubernetes expert. When possible, output a \
                kubectl command for the user to run at the end of your output. \
                Answer the user's questions based on your general knowledge of kubernetes, \
                the below context:\n\n{context} \n\n\
                and the following logs (if provided):\n\n{logs}",
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )

def create_bot(retriever):
    '''
    Create a bot with a retriever.
    '''
    retriever_chain = create_history_aware_retriever(llm, retriever, retriever_prompt)

    document_chain = create_stuff_documents_chain(llm, chat_prompt)

    qa = create_retrieval_chain(retriever_chain, document_chain)
    return qa

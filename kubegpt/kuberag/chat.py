# file: kubegpt/kuberag/chat.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from kubegpt.kuberag.tools import getAllTools

llm = ChatOpenAI(model="gpt-4")

chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful, concise chatbot and kubernetes expert. Use the tools you have at your disposal to \
                get information about kubernetes or to suggest a command to the user. \
                Answer the user's questions based on your general knowledge of kubernetes, with your tools, \
                and the following logs (if provided):\n\n{logs}",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

def create_bot(retriever):
    '''
    Create a bot with a retriever.
    '''
    tools = getAllTools(retriever)

    agent = create_openai_functions_agent(llm, tools, chat_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    return agent_executor
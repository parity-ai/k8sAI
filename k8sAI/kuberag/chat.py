# file: k8sAI/kuberag/chat.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from k8sAI.kuberag.tools import get_all_tools

llm = ChatOpenAI(model="gpt-4")

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful, concise chatbot and kubernetes expert. Use the tools you have at your disposal to \
                get information about kubernetes or to suggest a command to the user. \
                When possible and if provided, use the execute tool to gather more information about the cluster before answering. \
                If you use the execute tool, be sure to use the results in future answers and to fill in information and arguments. \
                If the user is providing a task to you, consider using the execute tool to solve it. \
                Refer to the chat history to check for relevant previous conversations and information. \
                Users can't see your tool call results, so be sure to state all findings at the end clearly. \
                If the user is requesting you to investigate a problem, use your knowledge as best you can to \
                follow the best practices for troubleshooting k8s. If you find an issue, suggest a fix! \
                If nothing is wrong, and the user asks for a fix, concisely let them know everything looks healthy.\
                Answer the user's questions based on your general knowledge of kubernetes, with your tools, \
                and the following logs (if provided):\n\n{logs}\n\
                Kubectl command output (optional):\n\n{command_output}",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("ai", "{agent_scratchpad}"),
    ]
)


def create_bot(retriever, disable_execution=False):
    """
    Create a bot with a retriever.
    """
    tools = get_all_tools(retriever, disable_execution=disable_execution)

    agent = create_openai_functions_agent(llm, tools, chat_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)

    memory = ChatMessageHistory(session_id="test-session")
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_chat_history

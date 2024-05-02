# file: k8sAI/kuberag/main.py
import os
import pkg_resources
from rich.padding import Padding
from rich.markdown import Markdown

from k8sAI.kuberag.chat import create_bot
from k8sAI.kuberag.retriever import load_retriever
from k8sAI.kuberag.tool_handler import registry
from k8sAI.util import console


def get_embeddings_path():
    """Get the absolute path to the embeddings directory."""
    resource_path = pkg_resources.resource_filename(__name__, "embeddings")
    return resource_path


class k8sAI:
    """
    k8sAI is a class that allows you to chat with a GPT model.
    It uses a retriever to find relevant information.
        Args:
            disable_execution (bool): If True, the bot cannot execute kubectl commands to help.
            embeddings_path (str): The path to the stored embeddings
    """

    def __init__(
        self,
        disable_execution: bool = False,
        embeddings_path: str = get_embeddings_path(),
    ):
        self.retriever = load_retriever(embeddings_path)
        self.bot = create_bot(self.retriever, disable_execution)

    def start_chat(
        self,
        prompt,
        command_output="",
        logs: str = "<no logs provided>",
        terminal=False,
    ):
        """
        Start a chat with the bot. User can end with 'exit'.
            Args:
                logs (str): The logs to provide to the bot.
        """
        additional_context = None
        while True:
            if prompt:
                user_prompt = prompt
                prompt = None
            else:
                user_prompt = input("Prompt: ")
            if user_prompt.lower() == "exit":
                break
            # result = self.bot.invoke()
            if additional_context != None:
                user_prompt = f"using this \n{additional_context} \nrespond to this: {user_prompt}"
                additional_context = None
            for chunk in self.bot.stream(
                {"input": user_prompt, "logs": logs, "command_output": command_output},
                config={"configurable": {"session_id": "<foo>"}},
            ):
                # Agent Action
                if "actions" in chunk:
                    for action in chunk["actions"]:
                        console.print(
                            Padding(
                                f":hammer: Calling Tool: `{action.tool}` with input `\
                                              {action.tool_input}`",
                                pad=(0, 0, 0, 2),
                            )
                        )
                # Observation
                elif "steps" in chunk:
                    continue
                # Final result
                elif "output" in chunk:
                    if registry.has_tool_handler(chunk["output"]):
                        additional_context, terminate = registry.use_handler(chunk["output"])
                        if terminate:
                            break
                    else:
                        console.print("k8sAI:")
                        console.print(Markdown(chunk["output"]))

                else:
                    raise ValueError()
                console.print("---")

            if terminal:
                break


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "k8sAI/kuberag/embeddings")
    k8sAI = k8sAI(embeddings_path=path)
    k8sAI.start_chat(None)

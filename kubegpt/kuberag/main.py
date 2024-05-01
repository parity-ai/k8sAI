# file: kubegpt/kuberag/main.py

import os
import pkg_resources
from kubegpt.kuberag.chat import create_bot
from kubegpt.kuberag.retriever import load_retriever
from kubegpt.kuberag.tool_handler import registry

def get_embeddings_path():
    """Get the absolute path to the embeddings directory."""
    resource_path = pkg_resources.resource_filename(__name__, "embeddings")
    return resource_path

class KubeGPT:
    '''
    KubeGPT is a class that allows you to chat with a GPT model. It uses a retriever to find relevant information.
        Args:
            disable_execution (bool): If True, the bot cannot execute kubectl commands to help.
            embeddings_path (str): The path to the stored embeddings
    '''
    def __init__(self, disable_execution: bool = False, embeddings_path: str = get_embeddings_path()):
        self.retriever = load_retriever(embeddings_path)
        self.bot = create_bot(self.retriever, disable_execution)

    def start_chat(self, prompt, command_output="", logs: str = "<no logs provided>", terminal=False):
        '''
        Start a chat with the bot. User can end with 'exit'.
            Args:
                logs (str): The logs to provide to the bot.
        '''
        while True:
            if prompt:
                user_prompt = prompt
                prompt = None
            else:
                user_prompt = input("Prompt: ")
            if user_prompt.lower() == "exit":
                break
            result = self.bot.invoke({"input": user_prompt, "logs": logs, "command_output": command_output})
            if registry.has_tool_handler(result['output']):
                terminate = registry.use_handler(result['output'])
                if terminate:
                    break

            print("\nKubeGPT: ", result['output'])
            if terminal:
                break

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "kubegpt/kuberag/embeddings")
    kubegpt = KubeGPT(path)
    kubegpt.start_chat(None, None)

# file: kubegpt/kuberag/main.py

import os
from kubegpt.kuberag.chat import create_bot
from kubegpt.kuberag.retriever import load_retriever
from kubegpt.kuberag.tool_handler import registry

class KubeGPT:
    '''
    KubeGPT is a class that allows you to chat with a GPT model. It uses a retriever to find relevant information.
        Args:
            embeddings_path (str): The path to the stored embeddings
    '''
    def __init__(self, embeddings_path: str = "kubegpt/kuberag/embeddings"):
        self.retriever = load_retriever(embeddings_path)
        self.bot = create_bot(self.retriever)

    def start_chat(self, prompt, logs: str = "<no logs provided>"):
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
            result = self.bot.invoke({"input": user_prompt, "logs": logs})
            if registry.has_tool_handler(result['output']):
                terminate = registry.use_handler(result['output'])
                if terminate:
                    break

            print("\nKubeGPT: ", result['output'])

if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "kubegpt/kuberag/embeddings")
    kubegpt = KubeGPT(path)
    kubegpt.start_chat(None)

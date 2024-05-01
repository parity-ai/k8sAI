# file: kubegpt/main.py
import click
from kubegpt.kuberag.main import KubeGPT

@click.group()
def chat_group():
    '''
    This tool uses OpenAI's ChatGPT to chat about Kubernetes. 
    It is enhanced with a retriever storing k8s documentation to improve results.
    It uses your OpenAI API key from $OPENAI_API_KEY to access the model.
    '''

@chat_group.command()
@click.option('--prompt', help='Initial prompt to start the conversation. (optional)')
def chat(prompt):
    """
    Start a conversation with the KubeGPT model.
    """
    kube_gpt = KubeGPT()  # Assume default embeddings path, modify as needed
    print("Starting conversation with KubeGPT...")
    print("Type 'exit' to end the conversation.")

    kube_gpt.start_chat(prompt)

def main():
    '''
    Main function for the CLI.
    '''
    chat_group()

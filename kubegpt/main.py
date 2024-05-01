# file: kubegpt/main.py
import click
from kubegpt.kuberag.main import KubeGPT
import subprocess

@click.group()
def chat_group():
    '''
    This tool uses OpenAI's ChatGPT to chat about Kubernetes. 
    It is enhanced with a retriever storing k8s documentation to improve results.
    It uses your OpenAI API key from $OPENAI_API_KEY to access the model.

    NOTE: This tool sends data to OpenAI's servers. Please review the OpenAI API terms of use.
    '''

@chat_group.command()
@click.option('-p', '--prompt', help='Initial prompt to start the conversation. (optional)')
@click.option('-t', '--terminal', is_flag=True, default=False, help='If terminal is enabled, kubeGPT will end the conversation (optional)')
def chat(prompt, terminal):
    """
    Start a conversation with the KubeGPT model. KubeGPT can suggest commands that can then be executed.
    """
    kube_gpt = KubeGPT()  # Assume default embeddings path, modify as needed
    print("Starting conversation with KubeGPT...")
    print("Type 'exit' to end the conversation.")

    kube_gpt.start_chat(prompt, terminal=terminal)

@chat_group.command()
@click.option('--cmd', help='Kubectl command that kubeGPT will explain the results of')
@click.option('-p', '--prompt', help='Additional prompt to go along with command output, otherwise default prompt is used (optional)')
@click.option('-t', '--terminal', is_flag=True, default=False, help='If terminal is enabled, kubeGPT will end the conversation (optional)')
def explain(cmd, prompt, terminal):
    """
    kubectl command will be executed and KubeGPT will explain the result
    """

    if not cmd.startswith("kubectl"):
        print("Error: Command must be kubectl command")
        return
    
    print(f"Running command: {cmd}")
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    print(f"Command output: {output}")

    if not prompt:
        prompt = "Concisely explain the output of the following command: " + cmd

    kube_gpt = KubeGPT()
    print("Explaining kubectl results with KubeGPT...")
    if not terminal:
        print("Type 'exit' to end the conversation.")

    kube_gpt.start_chat(prompt, command_output=output, terminal=terminal)


@chat_group.command()
@click.option('--cmd', help='Kubectl command that kubeGPT will use the results of')
@click.option('-p', '--prompt', help='Additional prompt to go along with command output, otherwise default prompt is used (optional)')
@click.option('-t', '--terminal', is_flag=True, default=False, help='If terminal is enabled, kubeGPT will end the conversation (optional)')
def fix(cmd, prompt, terminal):
    """
    kubectl command will be executed and KubeGPT will suggest a fix based on the output of the command
    """
    
    if not cmd.startswith("kubectl"):
        print("Error: Command must be kubectl command")
        return
    
    print(f"Running command: {cmd}")
    output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    print(f"Command output: {output}")

    if not prompt:
        prompt = "Based on the results of this command, suggest a fix (unless none is needed): " + cmd

    kube_gpt = KubeGPT()
    print("Looking for fix with KubeGPT...")
    if not terminal:
        print("Type 'exit' to end the conversation.")

    kube_gpt.start_chat(prompt, command_output=output, terminal=terminal)


def main():
    '''
    Main function for the CLI.
    '''
    chat_group()

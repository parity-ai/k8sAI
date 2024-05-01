# K9ai

K9ai is a RAG-enabled GPT that uses a vector store with the embeddings of the [Kubernetes documentation](https://kubernetes.io/docs/).
It can answer general questions about Kubernetes, explain output of provided kubectl commands, and suggested commands for you to then easily execute.
Given an issue, it can also use kubectl commands to understand the issue and suggest a fix.

<p align="center">
  <img src="https://github.com/wilson090/K9ai/assets/30668639/62549327-a4d2-44a0-8e85-2aa589582929">
</p>

K9ai has a few tools at its disposal that it can call to answer your questions and fix issues:
- `Execute_Kubectl_CMD_Tool` - KubeGPT can use this to execute kubectl read commands to gather more information about your cluster
- `Suggest_Kubectl_CMD_Tool` - KubeGPT uses this to suggest a kubectl command to you that you can then edit and execute
- `k8s_search` - This tool is used by KubeGPT to search k8s documentation to provide informed solutions

### Note:
This tool sends data to OpenAI's servers. Please review the OpenAI API terms of use before using this tool.
This tool also executes `kubectl` commands. While they should be read-only commands, unintended consequences are possible. Use the `--disable-execution` command if you want to be extra-safe.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install K9ai.

```bash
pip install k9ai
```

### Configuration

Before using K9ai, ensure your OpenAI API key is set as an environment variable (`OPENAI_API_KEY`).

## Usage
### Chat
To start a conversation with K9ai:
```bash
k9ai chat [OPTIONS]
```

Options:
- -p, --prompt Provide an initial prompt to start the conversation (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

### Explain
To have K9ai explain the output of a Kubernetes command:
```bash
k9ai explain --cmd='kubectl [command]' [OPTIONS]
```

Options:
- -p, --prompt Provide an additional prompt to go along with the command output (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

Note: Only `kubectl` commands are valid for explanation.

### Fix
To request K9ai to suggest a fix based on a provided description of the problem:
```bash
k9ai fix [OPTIONS]
```
If no prompt is provided, K9ai will attempt to discover the problem itself (under development)

Options:
- -p, --prompt A prompt describing the problem to analyze (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

Note: --disable-execution with signficantly reduce K9ai's ability to discover a problem. 

### Common Commands
```bash
# Start a chat session with K9ai
k9ai chat

# Explain the output a specific kubectl command, end chat after first response
k9ai explain --cmd='kubectl get pods' -t

# Suggest a fix for a described problem
k9ai fix --prompt='Pods in `default` namespace are crashing frequently'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This code is distributed under the AGPL v3 licensce.

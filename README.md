# k8sAI

k8sAI is a RAG-enabled GPT that uses a vector store with the embeddings of the [Kubernetes documentation](https://kubernetes.io/docs/).
It can answer general questions about Kubernetes, explain output of provided kubectl commands, and suggested commands for you to then easily execute.
Given an issue, it can also use kubectl commands to understand the issue and suggest a fix.

<p align="center">
  <img src="https://github.com/wilson090/k8sAI/assets/30668639/c7bf21a9-2912-4dfb-a6d1-c8e2da370c5f">
</p>

k8sAI has a few tools at its disposal that it can call to answer your questions and fix issues:
- `Execute_Kubectl_CMD_Tool` - k8sAI can use this to execute kubectl read commands to gather more information about your cluster
- `Suggest_Kubectl_CMD_Tool` - k8sAI uses this to suggest a kubectl command to you that you can then edit and execute
- `k8s_search` - This tool is used by k8sAI to search k8s documentation to provide informed solutions

### Note:
This tool sends data to OpenAI's servers. Please review the OpenAI API terms of use before using this tool.
This tool also executes `kubectl` commands. While they should be read-only commands, unintended consequences are possible. Use the `--disable-execution` command if you want to be extra-safe.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install k8sAI.

```bash
pip install k8sAI
```

### Configuration

Before using k8sAI, ensure your OpenAI API key is set as an environment variable (`OPENAI_API_KEY`).

## Usage
### Chat
To start a conversation with k8sAI:
```bash
k8sAI chat [OPTIONS]
```

Options:
- -p, --prompt Provide an initial prompt to start the conversation (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

### Explain
To have k8sAI explain the output of a Kubernetes command:
```bash
k8sAI explain --cmd='kubectl [command]' [OPTIONS]
```

Options:
- -p, --prompt Provide an additional prompt to go along with the command output (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

Note: Only `kubectl` commands are valid for explanation.

### Fix
To request k8sAI to suggest a fix based on a provided description of the problem:
```bash
k8sAI fix [OPTIONS]
```
If no prompt is provided, k8sAI will attempt to discover the problem itself (under development)

Options:
- -p, --prompt A prompt describing the problem to analyze (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

Note: --disable-execution with signficantly reduce k8sAI's ability to discover a problem. 

### Common Commands
```bash
# Start a chat session with k8sAI
k8sAI chat

# Explain the output a specific kubectl command, end chat after first response
k8sAI explain --cmd='kubectl get pods' -t

# Suggest a fix for a described problem
k8sAI fix --prompt='Pods in `default` namespace are crashing frequently'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This code is distributed under the AGPL v3 licensce.

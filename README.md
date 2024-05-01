# KubeAI

KubeAI is a RAG-enabled GPT that uses a vector store with the embeddings of the [Kubernetes documentation](https://kubernetes.io/docs/).
It can answer general questions about Kubernetes, explain or suggest fixes based on the output of kubectl commands, and provide suggested commands for you to then easily execute.

![Chat example](https://github.com/wilson090/KubeAI/assets/30668639/90afa809-9654-4f2a-be2c-371444b2c795)


### Note:
This tool sends data to OpenAI's servers. Please review the OpenAI API terms of use before using this tool.
This tool also executes `kubectl` commands. While they should be read-only commands, unintended consequences are possible. Use the `--disable-execution` command if you want to be extra-safe.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install KubeAI.

```bash
pip install kubeai
```

### Configuration

Before using KubeAI, ensure your OpenAI API key is set as an environment variable (`OPENAI_API_KEY`).

## Usage
### Chat
To start a conversation with KubeAI:
```bash
kubeai chat [OPTIONS]
```

Options:
- -p, --prompt Provide an initial prompt to start the conversation (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

### Explain
To have KubeAI explain the output of a Kubernetes command:
```bash
kubeai explain --cmd='kubectl [command]' [OPTIONS]
```

![Explain example](https://github.com/wilson090/KubeAI/assets/30668639/a900a77e-4997-4407-b20d-7773beeeb498)

Options:
- -p, --prompt Provide an additional prompt to go along with the command output (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

Note: Only `kubectl` commands are valid for explanation.

### Fix
To request KubeAI to suggest a fix based on a provided description of the problem:
```bash
kubeai fix [OPTIONS]
```
If no prompt is provided, KubeAI will attempt to discover the problem itself (under development)

![Fix example](https://github.com/wilson090/KubeAI/assets/30668639/a4f4bfd3-f996-4224-925d-0fa2a9207334)

Options:
- -p, --prompt A prompt describing the problem to analyze (optional)
- -t, --terminal Conversation will end after one response (optional)
- --disable-execution Disable execution of kubectl commands (optional)

Note: --disable-execution with signficantly reduce KubeAI's ability to discover a problem. 

### Common Commands
```bash
# Start a chat session with KubeAI
kubeai chat

# Explain the output a specific kubectl command, end chat after first response
kubeai explain --cmd='kubectl get pods' -t

# Suggest a fix for a described problem
kubeai fix --prompt='Pods in `default` namespace are crashing frequently'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

This code is distributed under the AGPL v3 licensce.

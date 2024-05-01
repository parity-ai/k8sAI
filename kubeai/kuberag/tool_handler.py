# file: kubeai/kuberag/tool_handler.py

import json
import os
from prompt_toolkit import prompt
from kubeai.util import console


class ToolHandlerRegistry:
    """
    A registry for tool handlers.
    """

    def __init__(self):
        self.registry = {}

    def register_tool(self, prefix, handler):
        """
        Register a tool with a prefix and handler function.
        """
        if prefix in self.registry:
            raise ValueError(f"Prefix {prefix} is already registered.")
        self.registry[prefix] = handler

    def has_tool_handler(self, input_string):
        """
        Check if the input string has a registered handler.
        """
        for prefix in self.registry:
            if input_string.startswith(prefix):
                return True
        return False

    def use_handler(self, input_string):
        """
        Parse the input string and return the result.
        """
        for prefix, handler in self.registry.items():
            if input_string.startswith(prefix):
                return handler(input_string, prefix)
        console.print("Error: No handler found for the input string.")
        return None


# TODO: create proper tool handler objects with data parse fn, etc.


def handle_kubectl_tool(input_string, prefix) -> bool:
    """
    Handle the kubectl tool data.

    returns: True if the tool should terminate. False otherwise
    """
    json_part = input_string[len(prefix) :]
    json_part = json_part.strip("'")

    try:
        data = json.loads(json_part)
        if "notes" in data:
            console.print("\n")
            console.print(data["notes"])
        if "query" in data:
            cmd = prompt(
                "Edit the cmd and press (enter) to run, \
                          leave empty to return to GPT\n\n",
                default=data["query"],
            )
            # Split the command into the command and its arguments for execvp
            args = cmd.split()

            # Check if any command is entered, then execute it
            if args:
                console.print("\n")
                # Replace the current process with the new command
                os.execvp(args[0], args)
            else:
                console.print("No command entered.")

    except json.JSONDecodeError:
        console.print("Error: The string is not valid JSON.", {json_part})

    return True


registry = ToolHandlerRegistry()
registry.register_tool("[Suggest_Kubectl_CMD_Tool]", handle_kubectl_tool)

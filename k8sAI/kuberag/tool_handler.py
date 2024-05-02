# file: k8sAI/kuberag/tool_handler.py

import json
import os
from prompt_toolkit import prompt
from k8sAI.util import console
import subprocess


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


def handle_suggest_kubectl_tool(input_string, prefix) -> bool:
    """
    Handle the kubectl tool data.

    returns: True if the tool should terminate. False otherwise
    """
    cmd_and_output = input_string[len(prefix) :]
    cmd_and_output = (cmd_and_output.strip("'")).split("||")
    output, cmd = cmd_and_output[0], cmd_and_output[1]
    
    context = f"{cmd} was just run and it outputed {output}"

    return context, False


registry = ToolHandlerRegistry()
registry.register_tool("[Suggest_Kubectl_CMD_Tool]", handle_suggest_kubectl_tool)

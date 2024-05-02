# file: k8sAI/kuberag/tools.py

import json
import re
import subprocess
from typing import Optional, Type
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools.retriever import create_retriever_tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from rich.padding import Padding
from k8sAI.util import console
from prompt_toolkit import prompt



def retriever_tool(retriever):
    """
    Create the retriever tool.
    """
    return create_retriever_tool(
        retriever,
        "k8s_search",
        "Search for information about Kubernetes via the official documentation.\
            For any questions about Kubernetes, you must use this tool!",
    )


class SuggestKubectlCommandInput(BaseModel):
    """
    Suggest kubectl command input.
    """

    notes: str = Field(
        description="Any notes that the user should know about the command \
                       (a short docstring would be helpful)."
    )
    query: str = Field(
        description="should be a kubectl command that the user wants to run."
    )


class SuggestKubectlCommandTool(BaseTool):
    """
    Suggest kubectl command tool.
    """

    name = "Suggest_Kubectl_CMD_Tool"
    description = "Suggest a kubectl command to the user. \
        This is a terminal command and will allow the user to \
        execute the command directly. They will be able to edit it before executing.\
        The command MUST be properly formatted, but it can contain placeholder values for the user to fill in. \
        Fill in values to the BEST of your ability (but if you don't know, use a placeholder) and if you can retrieve them with another tool, do that first! \
        This is a useful tool for suggesting commands to the user and you're very much encouraged to use it \
        if it answer's the user's question or solves their errors. If the user's question is more general, you should use the `k8s_search` \
        tool instead or answer the question directly."
    args_schema: Type[BaseModel] = SuggestKubectlCommandInput
    return_direct: bool = True

    def _run(
        self,
        notes: str,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # return this as a jsonified string so that we can parse and return it in the frontend
        data_dict = {"notes": notes, "query": query}
        if notes:
            console.print("\n")
            console.print(notes)
        if query:
            cmd = prompt(
                "Edit the cmd and press (enter) to run, leave empty to return to GPT\n\n",
                default=query,
            )
        args = cmd.split()

        # Check if any command is entered, then execute it
        if args:
            console.print("\n")
            try:
                output = subprocess.check_output(cmd, shell=True).decode("utf-8")
                console.print(output)
            except Exception as e:
                output = str(e)
        else:
            console.print("No command entered.")

        return f"[Suggest_Kubectl_CMD_Tool]{output}||{cmd}"

    async def _arun(
        self,
        notes: str,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Suggest Kubectl Command Tool does not support async")


class ExecuteKubectlCommandInput(BaseModel):
    command: str = Field(
        description="must be a properly formatted READ-ONLY kubectl command."
    )


class ExecuteKubectlCommandTool(BaseTool):
    name = "Execute_Kubectl_CMD_Tool"
    description = "Execute a kubectl command and receive the results. This allows you to retrieve info about the user's k8s \
    configuration in order to properly assit them. Anytime you need information about their cluster in order to inform \
    your decisions, use this tool by passing in a kubectl command. \
    When possible, use this tool over the suggest tool! Users appreciate that. \
    The results from this tool can be used to make better suggestions to the user, so this tool is extremely useful. \
    The command MUST be properly formatted. It can also only be a READ-ONLY command. \
    Under no circumstances should you modify underlying resources with this tool!!!"
    args_schema: Type[BaseModel] = ExecuteKubectlCommandInput
    return_direct: bool = False

    def _run(
        self, command: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        # execute command
        if not command.startswith("kubectl"):
            return "Error: Command must be kubectl command"

        allowed_patterns = [
            r"^kubectl get ",
            r"^kubectl describe ",
            r"^kubectl explain ",
            r"^kubectl top ",
            r"^kubectl api-resources",
            r"^kubectl api-versions",
            r"^kubectl version",
            r"^kubectl config view",
            r"^kubectl logs ",
        ]
        if not any(re.match(pattern, command) for pattern in allowed_patterns):
            return "Error: Command is not permitted, must be a read-only operation"

        try:
            console.print(
                Padding(f":gear: running command: {command}", pad=(0, 0, 0, 2))
            )
            output = subprocess.check_output(command, shell=True).decode("utf-8")
            console.print(Padding(":green_circle: command complete", pad=(0, 0, 0, 2)))
            return output
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(
        self,
        command: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Suggest Kubectl Command Tool does not support async")


def get_all_tools(retriever, disable_execution=False):
    """
    Get all tools.
    """
    tools = [retriever_tool(retriever), SuggestKubectlCommandTool()]
    if not disable_execution:
        tools.append(ExecuteKubectlCommandTool())
    return tools

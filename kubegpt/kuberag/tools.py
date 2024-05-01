# file: kubegpt/kuberag/tools.py

import json
from typing import Optional, Type
from langchain.tools.retriever import create_retriever_tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)

def retriever_tool(retriever):
    return create_retriever_tool(
        retriever,
        "k8s_search",
        "Search for information about Kubernetes via the official documentation.\
            For any questions about Kubernetes, you must use this tool!",
    )

class SuggestKubectlCommandInput(BaseModel):
    notes: str = Field(description="Any notes that the user should know about the command (a short docstring would be helpful).")
    query: str = Field(description="should be a kubectl command that the user wants to run.")

class SuggestKubectlCommandTool(BaseTool):
    name = "Suggest_Kubectl_CMD_Tool"
    description = "Suggest a kubectl command to the user. This is a terminal command and will allow the user to \
    execute the command directly. They will be able to edit it before executing.\
    The command MUST be properly formatted, but it can contain placeholder values for the user to fill in. \
    This is a useful tool for suggesting commands to the user and you're very much encouraged to use it \
    if it answer's the user's question or solves their errors. If the user's question is more general, you should use the `k8s_search` \
    tool instead or answer the question directly."
    args_schema: Type[BaseModel] = SuggestKubectlCommandInput
    return_direct: bool = True

    def _run(
        self,
        notes: str,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        # return this as a jsonified string so that we can parse and return it in the frontend
        data_dict = {
            "notes": notes,
            "query": query
        }

        # Convert the dictionary to a JSON string
        jsonified = json.dumps(data_dict)
        return f"[Suggest_Kubectl_CMD_Tool]{jsonified}"
    
    async def _arun(
        self,
        notes: str,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Suggest Kubectl Command Tool does not support async")



def getAllTools(retriever):
    '''
    Get all tools.
    '''
    return [retriever_tool(retriever), SuggestKubectlCommandTool()]
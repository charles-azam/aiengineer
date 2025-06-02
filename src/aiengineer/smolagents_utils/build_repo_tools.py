from pathlib import Path
import sys
from typing import Callable
from smolagents import tool

from aiengineer.utils.llm_edit_repo import (
    llm_edit_repo,
    llm_edit_files,
    llm_edit_folder,
    llm_fix_repo,
    get_repository_map,
    get_python_errors_and_print_outputs_in_repository,
    get_python_doc_as_markdown,
)
from aiengineer.smolagents_utils.prompts import get_prompt_aider_smolagents
from aiengineer.utils.parse_repository import FileAsObject

def build_repo_tools(
    repo_path: Path,
    litellm_id: str,
    original_task: str,
    edit_format: str = "diff",
    
) -> dict[str, Callable]:
    """
    Generate a dictionary mapping tool-names → @tool-decorated callables so that a
    smolagent can inspect, diagnose and auto-fix the repository located at
    ``repo_path``.

    Args:
        repo_path (Path):  Root directory of the repository.
        litellm_id (str):  The LiteLLM / OpenAI model identifier to use when the
                          underlying helper needs to call an LLM.

    Returns:
        dict[str, Callable]:  Ready-to-register smolagent tools.
    """
    prompt_aider = get_prompt_aider_smolagents(
        repo_name=repo_path.name,
        original_task=original_task,
    )
    tools: dict[str, Callable] = {}

    # ---------------------------------------------------------------------
    # Read-only helpers
    # ---------------------------------------------------------------------

    @tool
    def get_repository_map_tool(summary: bool = False) -> str:
        """Return a high-level of the repository.
        This includes the content of each file if you set `summary=False`, or a
        summary of each file if `summary=True`.
        
        This tool, along with the `get_individual_file_content_tool` are the only tools you can use to get access to the content of files in the repository.
        
        The files are given relative to the module. If you want to specify a file to another tool, use the same relative path given by this tool.
        
        If the module is called `my_module`, then the path will be given as `my_module/docs/my_doc.py`.
        
        
        Args:
            summary: If True, return a summary of each file instead of the full content.
        """
        return get_repository_map(repo_path=repo_path, summary=summary)

    tools["get_repository_map_tool"] = get_repository_map_tool
    
    @tool
    def get_individual_file_content_tool(file_path: str) -> str:
        """
        Return the content of a single file in the repository.
        
        **Always provide paths relative to the module.** You are inside a module. If the document you want is in `my_module/docs/my_doc.py`, then the expected value for `file_path` is `my_module/docs/my_doc.py`.
        
        Args:
            file_path: Relative path to the file in the repo.
        """
        return (repo_path / file_path).read_text()

    tools["get_individual_file_content_tool"] = get_individual_file_content_tool
    
    @tool
    def exec_all_python_files_tool() -> str:
        """
        Get a list of Python errors and print outputs in the repository.
        
        This tool will import all files in the repository and return a flat text with all the stdout and stderr outputs, as well as any Python errors encountered during the import.
        
        """
        return get_python_errors_and_print_outputs_in_repository(repo_path=repo_path)

    tools["exec_all_python_files_tool"] = exec_all_python_files_tool

    @tool
    def convert_python_doc_to_markdown(doc_path: str) -> str:
        """
        Render a pyforge Python file into markdown.
        
        Pyforge is a python library to write documents in python files, which can be rendered into markdown.
        
        You can use this tool to convert a Python file that contains pyforge documents into markdown.
        
        **Always provide paths relative to the module.** You are inside a module. If the document you want is in `my_module/docs/my_doc.py`, then the expected value for `doc_path` is `my_module/docs/my_doc.py`.

        Args:
            doc_path: Relative path to a .py pyforge doc file.
            
        """
        return get_python_doc_as_markdown(doc_path=doc_path, repo_path=repo_path)

    tools["convert_python_doc_to_markdown"] = convert_python_doc_to_markdown

    # ---------------------------------------------------------------------
    # Write / fix helpers (they mutate the repo on disk)
    # ---------------------------------------------------------------------

    @tool
    def llm_fix_repo_tool(
        optional_instructions: str = "",
    ) -> str:
        """
        Ask an LLM to auto-repair the codebase (imports, NameErrors, etc.).
        Returns a flat text description of problems it attempted to fix.
        
        This tool returns the python problems in a string. It is the same output as `exec_all_python_files_tool`. 
        This means that this tool WILL NOT be able to answer any question. So you must give instructions, not questions.
        This tool can work without `optional_instructions`, but you can provide additional context or instructions to the LLM to help it fix the repository. 

        Args:
            optional_instructions: Optional additional context or
                instructions to provide to the LLM for fixing the repository. By default, the llm will only be asked to fix the repository based on the errors it finds.
            
        """
        result = llm_fix_repo(
            repo_path=repo_path,
            litellm_id=litellm_id,
            additional_context_or_instructions=optional_instructions,
            repo_name=repo_path.name,
            edit_format=edit_format,
            system_context=prompt_aider,
        )
        return (
            result.convert_to_flat_txt()
            if result is not None
            else "No problems detected."
        )

    tools["llm_fix_repo_tool"] = llm_fix_repo_tool

    @tool
    def llm_edit_repo_tool(message: str) -> str:
        """
        Run an arbitrary instruction against the entire repo via LLM-powered aider.
        
        This tool returns None, this means that this tool WILL NOT be able to answer any question. So you must give instructions, not questions.

        
        Args:
            message: The instruction to run against the repo.
        """
        llm_edit_repo(
            message=message,
            repo_path=repo_path,
            litellm_id=litellm_id,
            repo_name=repo_path.name,
            edit_format=edit_format,
            system_context=prompt_aider,
        )
        return None

    tools["llm_edit_repo_tool"] = llm_edit_repo_tool

    @tool
    def llm_edit_files_tool(
        message: str,
        fnames: list[str],
    ) -> None:
        """
        Run an arbitrary instruction restricted to a list of files (relative paths) of repo via LLM-powered aider.
        
        **Always provide paths relative to the module.** You are inside a module. If the document you want is in `my_module/docs/my_doc.py`, then the expected value for `fnames` is [`my_module/docs/my_doc.py`].
        
        If you want to create a new file, just add the file name to the list, e.g. `["my_module/folder/new_file.py"]` and specify it to the LLM in the `message` parameter.
        
        This tool returns None, this means that this tool WILL NOT be able to answer any question. So you must give instructions, not questions.
        
        Args:
            message: The instruction to run against the repo.
            fnames: List of relative paths to files in the repo to restrict the LLM call to.
        """
        llm_edit_files(
            message=message,
            fnames=[FileAsObject._reconstruct_file_path(file_str=f, repo_path=repo_path) for f in fnames],
            repo_path=repo_path,
            litellm_id=litellm_id,
            repo_name=repo_path.name,
            edit_format=edit_format,
            system_context=prompt_aider,
        )
        return

    tools["llm_edit_files_tool"] = llm_edit_files_tool


    # TODO: give the direct possibility to modify the files, and use a benchmark to compare
    return tools

from aiengineer.config import EngineeringConfig
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool
from aiengineer.smolagents_utils.prompts import get_prompt_ai_engineer_smolagents, get_prompt_ai_engineer_smolagents_one_file
from aiengineer.smolagents_utils.build_repo_tools import build_repo_tools, RepoTool
from pathlib import Path

def create_smolagents_engineer_with_aider(config: EngineeringConfig) -> tuple[CodeAgent, str]:
    """
    Create a smolagent that can engineer a repository using the `pyforge` library.

    Args:
        repo_path (Path): The path to the repository to engineer.
        litellm_id (str): The LiteLLM / OpenAI model identifier to use.

    Returns:
        CodeAgent: A smolagent configured for engineering tasks.
    """
    
    
    repo_path = config.repo_path
    litellm_id = config.litellm_id
    iterations = config.iterations
    prompt = config.prompt

    tools = build_repo_tools(repo_path=repo_path, litellm_id=litellm_id, original_task=prompt)
    prompt = get_prompt_ai_engineer_smolagents(repo_name=repo_path.name, task=prompt)

    return CodeAgent(
        tools=list(tools.values()) + [
            DuckDuckGoSearchTool(),
            VisitWebpageTool()
        ],
        model=LiteLLMModel(litellm_id),
        max_steps=iterations,
        additional_authorized_imports=["*"]
    ), prompt
    
    
def create_smolagents_engineer_v2(config: EngineeringConfig, method = "diff") -> tuple[CodeAgent, str]:
    """Simplified version of the main agent that only directly calls the tools.

    Returns:
        tuple[CodeAgent, str]: A smolagent configured for engineering tasks.
    """
    
    repo_path = config.repo_path
    litellm_id = config.litellm_id
    iterations = config.iterations
    prompt = config.prompt
    
    def initialise_repo_smolagents_engineer_v2(repo_path: Path) -> None:
        """
        Initialise a repository for the smolagents engineer.
        """
        repo_path.mkdir(parents=True, exist_ok=True)
        (repo_path / "design.py").touch()
    
    initialise_repo_smolagents_engineer_v2(repo_path)
    
    tools = build_repo_tools(repo_path=repo_path, litellm_id=litellm_id, original_task=prompt)
    
    diff_tool = RepoTool.EDIT_FILE_DIFF
    if method == "whole":
        diff_tool = RepoTool.EDIT_FILE_WHOLE
    
    useful_tools_names: list[RepoTool] = [
        diff_tool,
        RepoTool.EXEC_FILE,
        RepoTool.EXEC_ALL_PYTHON_FILES,
        RepoTool.CONVERT_PYTHON_DOC_TO_MARKDOWN,
        RepoTool.GET_REPOSITORY_MAP,
        RepoTool.GET_INDIVIDUAL_FILE_CONTENT,
    ]
    
    useful_tools = [tools[tool_name.value] for tool_name in useful_tools_names]
    useful_tools.append(DuckDuckGoSearchTool())
    useful_tools.append(VisitWebpageTool())

    
    prompt = get_prompt_ai_engineer_smolagents_one_file(repo_name=repo_path.name, task=prompt)
    
    return CodeAgent(
        tools=useful_tools,
        model=LiteLLMModel(litellm_id),
        max_steps=iterations,
        additional_authorized_imports=["*"]

    ), prompt
    

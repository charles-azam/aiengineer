from aiengineer.config import EngineeringConfig
from smolagents import CodeAgent, LiteLLMModel, DuckDuckGoSearchTool, VisitWebpageTool
from aiengineer.smolagents_utils.prompts import get_prompt_ai_engineer_smolagents
from aiengineer.smolagents_utils.build_repo_tools import build_repo_tools

def create_smolagents_engineer(config: EngineeringConfig) -> tuple[CodeAgent, str]:
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

    tools = build_repo_tools(repo_path=repo_path, litellm_id=litellm_id)
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
    
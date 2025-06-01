from pathlib import Path

from smolagents import tool
from yaml import DocumentStartEvent

from aiengineer.prompts import get_prompt_ai_engineer_smolagents
from aiengineer.template.nuclear_reactor import CONFIG_REACTOR, PROMPT_REACTOR
from aiengineer.tools.call_llm_on_repo import (RepoAsObject, call_llm_on_repo,
                                               fix_repository)
from aiengineer.tools.engineer_agent import run_engineer_agent

SYSTEM_PROMPT = get_prompt_ai_engineer_smolagents(
    repo_name=CONFIG_REACTOR.repo_path.name
)
REPO_PATH = CONFIG_REACTOR.repo_path
LITELLM_ID = CONFIG_REACTOR.litellm_id


# Ideas:
# - le format de base de données sont les Documents
# - on a un document principal qui sera donné en prépromt
# - c'est le document en markdown qui est donné à l'agent principal
# - on a un agent maître qui choisit ce qu'il faut faire et des agents secondaires qui lancent des simulations
# - on a une fonction afin d'initialiser le projet avec des exemples
# - réfléchir à une structure simple pour les infos avec des simu autonomes'
# - add test with calls to smolagents "call this tool" and check the logs
@tool
def ask_coder_modification_on_repo_tool(question: str) -> None:
    """Asks a question to another agent that will modify the repository according to the instructions in the question.

    Args:
        question: The question to ask to the agent.
    """

    i = 0
    while fix_repository(REPO_PATH, litellm_id=LITELLM_ID) and i < 5:
        i += 1
        print(f"--- Attempt number {i} ---")

    # Call the LLM on the repository with the question
    run_engineer_agent(
        question=question,
        system_prompt=SYSTEM_PROMPT,
        repo_path=REPO_PATH,
        litellm_id=CONFIG_REACTOR.litellm_id,
    )

    i = 0
    while fix_repository(REPO_PATH, litellm_id=LITELLM_ID) and i < 5:
        i += 1
        print(f"--- Attempt number {i} ---")


@tool
def ask_coder_fix_the_code_tool() -> None:
    """Asks a question to another agent that will modify the repository according to the instructions in the question."""

    while fix_repository(REPO_PATH, litellm_id=LITELLM_ID) and i < 5:
        i += 1
        print(f"--- Attempt number {i} ---")


@tool
def get_codebase_as_markdown_tool() -> str:
    """Returns the codebase as a markdown string.

    Returns:
        The codebase as a markdown string.
    """

    # Call the LLM on the repository with the question
    repo = RepoAsObject.from_directory(repo_path=REPO_PATH)
    return repo.to_markdown()


@tool
def get_all_print_outputs_tool() -> str:
    """Executes all files in the repo and returns all the print outputs from the repository.

    Returns:
        The print outputs from the repository.
    """

    # Call the LLM on the repository with the question
    repo = RepoAsObject.from_directory(repo_path=REPO_PATH)
    outputs = repo.get_outputs_on_files(with_outputs=True, with_errors=True)
    if outputs:
        return outputs.convert_to_flat_txt() + "End of outputs"
    else:
        return "No outputs found."

import logging
from pathlib import Path

from aiengineer.tools.llm_edit_repo import (RepoAsObject, call_llm_on_repo,
                                               fix_repository)

logger = logging.getLogger(__name__)


def run_engineer_agent(
    repo_path: Path, question: str, system_prompt: str, litellm_id: str
):
    question = system_prompt + question
    call_llm_on_repo(message=question, repo_path=repo_path, litellm_id=litellm_id)


def iterative_engineering_process(
    repo_path: Path,
    question: str,
    system_prompt: str,
    litellm_id: str,
    iterations: int = 5,
    trials: int = 5,
):
    for iteration in range(iterations):
        logger.info(f"--- Running iteration number {iteration} ---")
        i = 0
        while fix_repository(repo_path, litellm_id=litellm_id) and i < trials:
            i += 1
            logger.warning(f"--- Attempt fix number {i} ---")

        repo = RepoAsObject.from_directory(repo_path=repo_path)
        outputs = repo.get_outputs_on_files(with_outputs=True, with_errors=True)
        if outputs:
            question = f"""
Outputs from the previous iteration:
{outputs.convert_to_flat_txt()}
End of outputs

Question:
{question}
"""

        run_engineer_agent(
            question=question,
            repo_path=repo_path,
            system_prompt=system_prompt,
            litellm_id=litellm_id,
        )

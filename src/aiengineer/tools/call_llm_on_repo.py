from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
from pathlib import Path
from aiengineer.tools.parse_repository import RepoAsJson, RepoAsObject
from aiengineer.prompts import get_prompt_fix_repository    

def call_llm_on_repo(message: str, repo_path: Path, litellm_id :str, repo_name: str | None = None, edit_format: str = "diff") -> None:
    input = """
# Repository context  (read *before* writing code)
• You are working **inside a Python package named `{my_repo}`**.  
• A file called `{my_repo}/__init__.py` already exists, so everything in this repo is import-able as `{my_repo}.<module>`.  
• **Rule #1 (imports)** – Whenever one module imports another *within this repo*, use an **absolute package import** that starts with `{my_repo}.`.  
  ✗ Do **NOT** write `import a`, `from a import …`, `from .a import …`, or any relative import.  
  ✓ Instead write `from {my_repo} import a` or `from {my_repo}.a import a`.  
• Follow PEP 8 unless a rule above overrides it.  
• After writing the files, do not output anything except the code blocks.

# Task
{task}
"""
    message = input.format(my_repo=repo_name or repo_path.name, task=message)
    
    sub_project_file_names = list(repo_path.rglob("*.py"))
    
    io = InputOutput(yes=True)
    fnames = sub_project_file_names
    
    model = Model(model=litellm_id,)
    model.use_repo_map = False
    model.edit_format = edit_format
    
    coder: Coder = Coder.create(main_model=model, fnames=fnames, auto_commits=False, use_git=False, io=io, suggest_shell_commands=False)
    
    coder.run_one(user_message=message, preproc=False)
    return


def fix_repository(repo_path: Path, litellm_id: str) -> RepoAsJson | None:
    repo = RepoAsObject.from_directory(repo_path=repo_path)
    problems: RepoAsJson = repo.get_outputs_on_files(with_errors=True, with_outputs=False)

    if problems:
        print("❌ Trying and fix the problem")
        print(problems.convert_to_flat_txt())
        message = get_prompt_fix_repository(repo_name=repo_path.name)
        message += problems.convert_to_flat_txt()
        call_llm_on_repo(message=message, repo_path=repo_path, litellm_id=litellm_id)
    else:
        print("✅ no Problems found ")
        return None

    return problems




from ast import main
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
from pathlib import Path
from aiengineer.tools.parse_repository import RepoAsJson, RepoAsObject
import logging
logger = logging.getLogger(__name__)

def call_llm_on_repo_with_files(message: str, fnames: list[Path], repo_path: Path, litellm_id :str, repo_name: str | None = None, edit_format: str = "diff") -> None:
    assert repo_path.is_dir()
    assert repo_path.exists(), f"The repository path {repo_path} does not exist."
    main_init_file = repo_path/"__init__.py"
    assert main_init_file.exists(), "The repository must have an __init__.py file to be a valid Python package."
    
    if main_init_file not in fnames:
        fnames.append(main_init_file)
        
    template_message = """
# Repository context  (read *before* writing code)
• You are working **inside a Python package named `{my_repo}`**.  
• A file called `{my_repo}/__init__.py` already exists, so everything in this repo is import-able as `{my_repo}.<module>`.  
• **Rule #1 (imports)** – Whenever one module imports another *within this repo*, use an **absolute package import** that starts explicitly with `{my_repo}.<submodule>`.  
  ✗ Do **NOT** write `import a`, `from a import …`, `from .a import …`, or any relative import.  
  ✓ Instead write `from {my_repo}.your_submodule import a` or `from {my_repo}.your_submodule.a import a`.  
• Follow PEP 8 unless a rule above overrides it.  
• After writing the files, do not output anything except the code blocks.

# Task
{task}
"""
    message = template_message.format(my_repo=repo_name or repo_path.name, task=message)
    
    io = InputOutput(yes=True)
    
    model = Model(model=litellm_id,)
    model.use_repo_map = False
    model.edit_format = edit_format
    
    coder: Coder = Coder.create(main_model=model, fnames=fnames, auto_commits=False, use_git=False, io=io, suggest_shell_commands=False)
    
    coder.run_one(user_message=message, preproc=False)
    

def call_llm_on_repo_with_folder(message: str, folder_path: Path, repo_path: Path, litellm_id :str, repo_name: str | None = None, edit_format: str = "diff") -> None:
    file_names = list(folder_path.rglob("*.py"))
    if not file_names:
        raise ValueError(f"No Python files found in the repository at {folder_path}.")
    call_llm_on_repo_with_files(message=message, fnames=file_names, repo_path=repo_path, litellm_id=litellm_id, repo_name=repo_name, edit_format=edit_format)
    
def call_llm_on_repo(message: str, repo_path: Path, litellm_id :str, repo_name: str | None = None, edit_format: str = "diff") -> None:
    call_llm_on_repo_with_folder(message=message, folder_path=repo_path, repo_path=repo_path, litellm_id=litellm_id, repo_name=repo_name, edit_format=edit_format)
    
    

def fix_repository(repo_path: Path, litellm_id :str, repo_name: str | None = None, edit_format: str = "diff") -> RepoAsJson | None:
    repo = RepoAsObject.from_directory(repo_path=repo_path)
    problems: RepoAsJson = repo.get_outputs_on_files(with_errors=True, with_outputs=False)
    task_template = """
The python code in the repository is incorrect. Your job is to fix them. 

Please remember that all files are inside a repository so all imports must start with from {repo_name}.

You are inside an interation so do not hesite to add some prints for the next iteration
Here is a list of errors per file:
"""

    
    repo_name = repo_name or repo_path.name
    
    task = task_template.format(repo_name=repo_name)

    if problems:
        logger.warning("❌ Trying and fix the problem")
        logger.warning(problems.convert_to_flat_txt())
        
        message += problems.convert_to_flat_txt()
        call_llm_on_repo(message=message, repo_path=repo_path, litellm_id=litellm_id, repo_name=repo_name, edit_format=edit_format)
    else:
        logger.info("✅ no Problems found ")
        return None

    return problems




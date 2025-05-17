from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
from pathlib import Path
from aiengineer.tools.parse_repository import RepoAsJson, RepoAsObject
from aiengineer.prompts import get_prompt_fix_repository    

def call_llm_on_repo(message: str, repo_path: Path, litellm_id :str):
    sub_project_file_names = list(repo_path.rglob("*.py"))
    
    io = InputOutput(yes=True)
    fnames = sub_project_file_names
    
    model = Model(model=litellm_id,)
    model.use_repo_map = False
    model.edit_format = "diff"
    
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




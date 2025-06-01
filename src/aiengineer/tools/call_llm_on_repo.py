import logging
import random
import tempfile
from ast import main
from operator import add
from pathlib import Path
from pydoc import doc

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model

from aiengineer.tools.parse_repository import RepoAsJson, RepoAsObject

logger = logging.getLogger(__name__)


def call_llm_on_repo_with_files(
    message: str,
    fnames: list[Path],
    repo_path: Path,
    litellm_id: str,
    repo_name: str | None = None,
    edit_format: str = "diff",
) -> None:
    assert repo_path.is_dir()
    assert repo_path.exists(), f"The repository path {repo_path} does not exist."
    main_init_file = repo_path / "__init__.py"
    assert (
        main_init_file.exists()
    ), "The repository must have an __init__.py file to be a valid Python package."

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

    model = Model(
        model=litellm_id,
    )
    model.use_repo_map = False
    model.edit_format = edit_format

    coder: Coder = Coder.create(
        main_model=model,
        fnames=fnames,
        auto_commits=False,
        use_git=False,
        io=io,
        suggest_shell_commands=False,
    )

    coder.run_one(user_message=message, preproc=False)


def call_llm_on_repo_with_folder(
    message: str,
    folder_path: Path,
    repo_path: Path,
    litellm_id: str,
    repo_name: str | None = None,
    edit_format: str = "diff",
) -> None:
    file_names = list(folder_path.rglob("*.py"))
    if not file_names:
        raise ValueError(f"No Python files found in the repository at {folder_path}.")
    call_llm_on_repo_with_files(
        message=message,
        fnames=file_names,
        repo_path=repo_path,
        litellm_id=litellm_id,
        repo_name=repo_name,
        edit_format=edit_format,
    )


def call_llm_on_repo(
    message: str,
    repo_path: Path,
    litellm_id: str,
    repo_name: str | None = None,
    edit_format: str = "diff",
) -> None:
    call_llm_on_repo_with_folder(
        message=message,
        folder_path=repo_path,
        repo_path=repo_path,
        litellm_id=litellm_id,
        repo_name=repo_name,
        edit_format=edit_format,
    )


def get_repo_as_json_output(
    repo_path: Path, with_errors: bool = False, with_outputs: bool = False
) -> RepoAsJson:
    repo = RepoAsObject.from_directory(repo_path=repo_path)
    outputs = repo.get_outputs_on_files(
        with_errors=with_errors, with_outputs=with_outputs
    )
    return outputs


def get_python_errors_in_repository(repo_path: Path) -> str:
    repo_as_json = get_repo_as_json_output(
        repo_path=repo_path, with_errors=True, with_outputs=True
    )
    return repo_as_json.convert_to_flat_txt()


def get_print_outputs_in_repository(repo_path: Path) -> str:
    repo_as_json = get_repo_as_json_output(
        repo_path=repo_path, with_errors=False, with_outputs=True
    )
    return repo_as_json.convert_to_flat_txt()


def fix_repository(
    repo_path: Path,
    litellm_id: str,
    additional_context_or_instructions: str = "",
    repo_name: str | None = None,
    edit_format: str = "diff",
) -> RepoAsJson | None:
    task_template = """
## Fix Python code in repository:

The code in the repository `{repo_name}` contains errors. Fix these issues with the following guidelines:

- **Absolute Imports:** Ensure all imports within the repository use absolute imports starting explicitly with `from {repo_name}.`
  ✗ Avoid: `import module`, `from .module import x`, etc.
  ✓ Correct: `from {repo_name}.module import x`

- **Common fixes needed:** Resolve import errors, `NameError`, `SyntaxError`, and other issues listed explicitly below.

- **Debugging statements:** Add clear and helpful `print()` statements as necessary to facilitate debugging in future iterations. Clearly indicate their purpose.

## Errors to fix:
{errors_to_fix}

"""
    additional_context_or_instructions_template = """

## Additional context or instructions:
{additional_context_or_instructions}
"""

    repo_name = repo_name or repo_path.name

    problems = get_repo_as_json_output(
        repo_path=repo_path, with_errors=True, with_outputs=False
    )

    if problems:
        output_message = get_python_errors_in_repository(repo_path=repo_path)
        logger.warning("❌ Trying and fix the problem")
        logger.warning(output_message)

        message = task_template.format(
            repo_name=repo_name, errors_to_fix=output_message
        )
        if additional_context_or_instructions:
            additional_context_or_instructions_message = additional_context_or_instructions_template.format(
                additional_context_or_instructions=additional_context_or_instructions
            )
            message += "\n" + additional_context_or_instructions_message
        call_llm_on_repo(
            message=message,
            repo_path=repo_path,
            litellm_id=litellm_id,
            repo_name=repo_name,
            edit_format=edit_format,
        )
    else:
        logger.info("✅ no Problems found ")
        return None

    return problems


def get_repository_map(repo_path: Path) -> str:
    repo = RepoAsObject.from_directory(repo_path=repo_path, with_summary=True)
    repo_as_json = repo.to_repo_as_json(summary=True)
    return repo_as_json.convert_to_flat_txt()


def get_python_doc_as_markdown(doc_path: Path | str, repo_path: Path) -> str:
    from pyforge.cli import markdown

    if isinstance(doc_path, Path):
        doc_path_str = str(doc_path.relative_to(repo_path))
    else:
        doc_path_str = doc_path
        doc_path = Path(doc_path)
        if not doc_path.is_absolute():
            doc_path = repo_path / doc_path

    repo_as_object = RepoAsObject.from_directory(repo_path=repo_path)
    repo_as_json = repo_as_object.to_repo_as_json()
    repo_as_dict = repo_as_json.to_dict()
    if doc_path_str not in repo_as_dict:
        raise ValueError(
            f"""The document {doc_path_str} is not found in the repository {repo_path}.
Here is the list of files in the repository:
{"\n".join(list(repo_as_dict.keys()))}
                         """
        )
    output = doc_path.with_suffix(".md")
    markdown(doc_path=doc_path, output_path=output)
    output_text = output.read_text()

    # TODO: handle images correctly
    return output_text

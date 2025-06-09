import logging
from pathlib import Path

from aiengineer.utils.parse_repository import FileAsObject, RepoAsJson, RepoAsObject

logger = logging.getLogger(__name__)



def get_repo_as_json_output(
    repo_path: Path, with_errors: bool = False, with_outputs: bool = False
) -> RepoAsJson:
    repo = RepoAsObject.from_directory(repo_path=repo_path)
    outputs = repo.get_outputs_on_files(
        with_errors=with_errors, with_outputs=with_outputs
    )
    return outputs


def get_python_errors_and_print_outputs_in_repository(repo_path: Path) -> str:
    repo_as_json = get_repo_as_json_output(
        repo_path=repo_path, with_errors=True, with_outputs=True
    )
    if repo_as_json:
        return repo_as_json.convert_to_flat_txt()
    else:
        return ""


def get_print_outputs_in_repository(repo_path: Path) -> str:
    repo_as_json = get_repo_as_json_output(
        repo_path=repo_path, with_errors=False, with_outputs=True
    )
    return repo_as_json.convert_to_flat_txt()


def get_repository_map(repo_path: Path, summary: bool = False) -> str:
    repo = RepoAsObject.from_directory(repo_path=repo_path, with_summary=summary)
    repo_as_json = repo.to_repo_as_json(summary=summary)
    return repo_as_json.convert_to_flat_txt()


def get_python_doc_as_markdown(doc_path: Path | str, repo_path: Path) -> str:
    from pyforge.cli import markdown

    if isinstance(doc_path, Path):
        doc_path_str = FileAsObject.reduce_file_path(file_path=doc_path, repo_path=repo_path)
    else:
        doc_path_str = doc_path
        doc_path = Path(doc_path)
        if not doc_path.is_absolute():
            doc_path = FileAsObject._reconstruct_file_path(file_str=doc_path, repo_path=repo_path)

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

from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import sys
import traceback
from dataclasses import asdict, dataclass
from pathlib import Path

from pydantic import BaseModel, Field


def sorted_rglob(input: Path, pattern: str = "*.py") -> list[Path]:
    return list(input.rglob(pattern=pattern))


class FileAsJson(BaseModel):
    """
    This is the representation of a file in the class, it contains both the name of the file and its content
    """

    name: str = Field(description="The name of the file")
    content: str | None = Field(
        description="The content of the file, null means the file must be removed"
    )


class RepoAsJson(BaseModel):
    """
    This class is supposed to represent a repo structure.
    The json equivalent of this class looks like this
    {
      "files": [
        {
          "name": "<filename.py>",
          "content": "<the revised file content>"
        },
        ...
      ]
    }
    You must answer with only the modified files, where "name" is the file name and "content" is the updated content. If no modifications are needed, return an empty object.
    """

    files: list[FileAsJson] = Field(description="List of files in the repo")

    def to_dict(self) -> dict[str, FileAsJson]:
        output = {}
        for file in self.files:
            if file.name in output:
                raise AttributeError(
                    f"Can't have two files with the same name {file.name}"
                )
            else:
                output[file.name] = file
        return output

    def convert_to_flat_txt(self) -> str:
        message = ""
        for file in self.files:
            message += f"\n\n**{file.name}**: \n"
            message += file.content
        return message


class FileAsObject(BaseModel):
    """
    Représente un fichier dans le repo.
    """

    repo_path: Path
    file_path_str: str
    file_content: str | None = None
    file_summary: str | None = None

    @classmethod
    def from_path(
        cls,
        file_path: Path,
        repo_path: RepoAsObject,
        file_content: str,
        file_summary: str,
    ):
        file_path_str = FileAsObject.reduce_file_path(
            file_path=file_path, repo_path=repo_path
        )
        return FileAsObject(
            repo_path=repo_path,
            file_path_str=file_path_str,
            file_content=file_content,
            file_summary=file_summary,
        )

    @property
    def file_path(self) -> Path:
        return FileAsObject._reconstruct_file_path(
            file_str=self.file_path_str, repo_path=self.repo_path
        )

    @staticmethod
    def reduce_file_path(file_path: Path, repo_path: Path) -> str:
        relative_path = file_path.relative_to(repo_path)
        return str(relative_path)

    @staticmethod
    def _reconstruct_file_path(file_str: str, repo_path: Path) -> Path:
        # TODO: fix this by not including the parent in the path to avoid mistakes
        return repo_path / Path(file_str)

    def to_file_as_json(self, summary: bool = False) -> FileAsJson:
        if summary:
            content = self.file_summary
        else:
            content = self.file_content
        return FileAsJson(name=self.file_path_str, content=content)


class RepoAsObject(BaseModel):
    repo_path: Path
    files: list[FileAsObject]

    def update_summaries(self):
        for file in self.files:
            file.file_summary = _create_summary_python_file(
                file_path=file.file_path,
                include_header=True,
            )

    @classmethod
    def from_directory(
        cls, repo_path: Path, with_summary: bool = False
    ) -> RepoAsObject:
        repo_files = []
        for file_path in sorted_rglob(repo_path):
            if not file_path.exists():
                raise FileNotFoundError(str(file_path))
            else:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
            summary = ""
            if with_summary:
                summary = _create_summary_python_file(
                    file_path=file_path,
                    include_header=True,
                )

            repo_files.append(
                FileAsObject.from_path(
                    repo_path=repo_path,
                    file_path=file_path,
                    file_content=content,
                    file_summary=summary,
                )
            )

        return cls(repo_path=repo_path, files=repo_files)

    def save_to_repo_path(
        self,
    ):
        """
        Override directory with new data
        """
        assert self.repo_path.exists()
        for file in self.files:
            os.makedirs(file.file_path.parent, exist_ok=True)
            file.file_path.write_text(file.file_content)

    def to_markdown(self) -> str:
        outputs = []
        for file in self.files:
            outputs.append(
                f"""
**{file.file_path_str}**:
```python
{file.file_content}
```
"""
            )
        return "\n".join(outputs)

    def to_repo_as_json(self, summary: bool = False) -> RepoAsJson:
        json_files = [f.to_file_as_json(summary=summary) for f in self.files]
        return RepoAsJson(files=json_files)

    @classmethod
    def from_repo_as_json(
        cls, repo_as_json: RepoAsJson, repo_path: Path
    ) -> RepoAsObject:
        repo_files = [
            FileAsObject(
                file_path_str=file.name, repo_path=repo_path, file_content=file.content
            )
            for file in repo_as_json.files
        ]
        return cls(repo_path=repo_path, files=repo_files)

    def get_outputs_on_files(
        self, with_outputs: bool = False, with_errors: bool = True
    ) -> RepoAsJson | None:
        """
        Import all Python files in a given repository to verify they load without errors,
        capturing printed outputs during their execution.

        Args:
            repo_path (Path): Path to the repository.

        Returns:
            dict: A dictionary with file paths as keys and their status ("Success" or the error message and output) as values.
        """
        results = []

        for file in self.files:
            content = ""
            file_path = file.file_path
            module_name = (
                file_path.relative_to(self.repo_path)
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
            )
            output_buffer = io.StringIO()  # Buffer to capture printed output
            original_stdout = sys.stdout  # Save original stdout
            file_name = file.file_path_str
            try:
                # Redirect stdout to the buffer
                sys.stdout = output_buffer

                # Dynamically load the Python file
                spec = importlib.util.spec_from_file_location(
                    module_name, str(file_path)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Capture success message and output*
                output = output_buffer.getvalue()
                if output and with_outputs:
                    content += output
            except Exception as e:
                # Capture error message and output
                output = output_buffer.getvalue()
                output_message = ""
                if output:
                    output_message = f"STDOUT:\n{output_buffer.getvalue()}"
                error = f"Error: {traceback.format_exc()}\n{output_message}"
                if with_errors:
                    content += error
            finally:
                # Restore original stdout
                sys.stdout = original_stdout
                output_buffer.close()
                if len(content) > 0:
                    results.append(FileAsJson(name=file_name, content=content))

        if results:
            return RepoAsJson(files=results)
        else:
            return None


def _create_summary_python_file(
    file_path: Path, include_header: bool = True, include_docstring: bool = True
):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    # Extract components
    header = ast.get_docstring(tree) if include_header else ""
    functions = []
    classes = []
    variables = []

    # Process top-level nodes
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append(
                _get_signature_with_docstring(
                    node, source, include_docstring=include_docstring
                )
            )
        elif isinstance(node, ast.ClassDef):
            classes.append(
                _get_signature_with_docstring(
                    node, source, include_docstring=include_docstring
                )
            )
        elif isinstance(node, ast.Assign):
            variables.append(_get_signature(node, source))

    # Build summary
    summary = []
    if include_header and header:
        summary.append(f"Module Description:\n{header}\n")
    if classes:
        summary.append("Classes:\n" + "\n".join(classes) + "\n")
    if functions:
        summary.append("Functions:\n" + "\n".join(functions) + "\n")
    if variables:
        summary.append("Variables:\n" + "\n".join(variables) + "\n")
    return "\n".join(summary).strip()


def _get_signature(node: ast.AST, source: str) -> str:
    """Helper to extract signatures from source code"""
    lines = source.split("\n")
    start_line = node.lineno - 1  # Convert to 0-based index

    if isinstance(node, ast.Assign):
        # Return first line of assignment
        return lines[start_line].strip()
    else:
        # Handle functions/classes (capture until colon)
        signature_lines = []
        for i in range(start_line, len(lines)):
            line = lines[i]
            code_part = line.split("#", 1)[0].rstrip()
            signature_lines.append(line)
            if code_part.endswith(":"):
                break
        return "\n".join(signature_lines).strip()


def _get_signature_with_docstring(
    node: ast.AST, source: str, include_docstring: bool = True
) -> str:
    """
    Helper to extract signatures along with their docstrings from source code.
    """
    signature = _get_signature(node, source)
    docstring = ast.get_docstring(node)
    if docstring and include_docstring:
        signature += f'\n"""\n{docstring}\n"""'
    return signature

import logging

from pathlib import Path

logger = logging.getLogger(__name__)

def direct_edit_file_diff(file_path: Path, string_to_replace: str, replacement: str) -> str:
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
    file_content = file_path.read_text()
    new_content = file_content.replace(string_to_replace, replacement)
    file_path.write_text(new_content)
    return new_content

def direct_edit_file_whole(
    file_path: Path,
    new_content: str,
) -> None:
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()
    file_path.write_text(new_content)
    
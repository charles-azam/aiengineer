"""
Most software engineers would rather use fixtures instead of a simple testing file/folder.

But I can't help it, I hate fixtures. It is harder to debug And I find it hard to explain to beginners.
"""
import shutil
from pathlib import Path
from aiengineer.common import AIENGINEER_SRC_DIR

TESTING_PATH = AIENGINEER_SRC_DIR / "testing"
TESTING_MODEL = "bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0"

def generate_testing_folder(testing_path: Path):
    """
    Generate a testing folder for the AI Engineer project.
    """
    if not testing_path.exists():
        testing_path.mkdir(parents=True, exist_ok=True)
    return testing_path
    
def initialise_empty_folder(folder_path: Path):
    shutil.rmtree(folder_path, ignore_errors=True)
    shutil.rmtree(folder_path.parent, ignore_errors=True)
    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / "__init__.py").touch()
    (folder_path.parent / "__init__.py").touch()
    
def initialise_folder_with_code() -> Path:
    testing_dir = TESTING_PATH / "fix_repository"
    initialise_empty_folder(testing_dir)
    
    file = testing_dir / "conversion.py"
    file.write_text(
    """
from fix_repository.values import masse_kg

def convert_kg_to_g(a: float):
    return a * 100


masse_g = convert_kg_to_g(masse_kg)

assert masse_g*1000 == masse_kg       
    """
        )
    file = testing_dir / "values.py"
    file.write_text(
    """
masse_kg = 10
print(masse_kg)
    """
        )
    return testing_dir
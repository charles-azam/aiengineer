"""
Most software engineers would rather use fixtures instead of a testing file/folder.

But I can't help it, I hate fixtures. And I find it hard to explain to beginners.
"""

from pathlib import Path
from pytest import fixture
from aiengineer.common import AIENGINEER_SRC_DIR

TESTING_PATH = AIENGINEER_SRC_DIR / "testing"
TESTING_MODEL = "openai/gpt-4o"

def generate_testing_folder(testing_path: Path):
    """
    Generate a testing folder for the AI Engineer project.
    """
    if not testing_path.exists():
        testing_path.mkdir(parents=True, exist_ok=True)
    return testing_path
    

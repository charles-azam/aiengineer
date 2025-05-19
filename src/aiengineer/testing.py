from pathlib import Path
from pytest import fixture
from aiengineer.common import AIENGINEER_SRC_DIR

TESTING_PATH = AIENGINEER_SRC_DIR / "testing"

def generate_testing_folder(testing_path: Path):
    """
    Generate a testing folder for the AI Engineer project.
    """
    if not testing_path.exists():
        testing_path.mkdir(parents=True, exist_ok=True)
    return testing_path
    

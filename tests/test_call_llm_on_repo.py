from aiengineer.testing import TESTING_PATH, TESTING_MODEL
import shutil
from pathlib import Path
from aider.repo import GitRepo

from aiengineer.tools.call_llm_on_repo import call_llm_on_repo, call_llm_on_repo_with_folder, fix_repository, call_llm_on_repo_with_files, RepoAsObject, RepoAsJson, get_prompt_fix_repository

def initialise_folder(folder_path: Path):
    shutil.rmtree(folder_path, ignore_errors=True)
    shutil.rmtree(folder_path.parent, ignore_errors=True)
    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / "__init__.py").touch()
    (folder_path.parent / "__init__.py").touch()
    
def initialise_folder_for_testing() -> Path:
    testing_dir = TESTING_PATH / "fix_repository"
    initialise_folder(testing_dir)
    
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
    """
        )
    return testing_dir

def test_call_llm_on_repo():
    testing_dir = TESTING_PATH / "call_llm_on_repo"
    initialise_folder(testing_dir)
    call_llm_on_repo(
        message="""
Create three files:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b` using the `my_repo.` prefix.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.

""",
        repo_path=testing_dir,
        litellm_id=TESTING_MODEL,
        repo_name="testing.call_llm_on_repo",
    )
    from testing.call_llm_on_repo import a, b, c
    from testing.call_llm_on_repo.c import a, b, c
    assert c == 3
    
def test_call_llm_on_repo_with_files():
    testing_dir = TESTING_PATH / "call_llm_on_repo_with_files"
    initialise_folder(testing_dir)
    call_llm_on_repo_with_files(
        message="""
Create three files in a directory named call_llm_on_repo_with_files:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b` using the `my_repo.` prefix.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.
4. **__init__.py** – create an empty file to make the directory importable.

""",
        fnames=[testing_dir / "a.py", testing_dir / "b.py", testing_dir / "c.py"],
        repo_path=TESTING_PATH,
        litellm_id=TESTING_MODEL,
    )
    from testing.call_llm_on_repo_with_files import a, b, c
    from testing.call_llm_on_repo_with_files.c import a, b, c
    assert c == 3

    
def test_call_llm_on_repo_with_folder():
    testing_dir = TESTING_PATH / "call_llm_on_repo_with_folder"
    initialise_folder(testing_dir)
    call_llm_on_repo_with_folder(
        message="""
Create three files in a directory named call_llm_on_repo_with_folder:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b` using the `my_repo.` prefix.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.

""",
        folder_path=testing_dir,
        repo_path=TESTING_PATH,
        litellm_id=TESTING_MODEL,
    )
    from testing.call_llm_on_repo_with_folder import a, b, c
    from testing.call_llm_on_repo_with_folder.c import a, b, c
    assert c == 3
    
def test_fix_repository():
    testing_dir = initialise_folder_for_testing()
    from aiengineer.tools.call_llm_on_repo import fix_repository
    fix_repository(repo_path=testing_dir, litellm_id=TESTING_MODEL, edit_format="diff")
    
def test_fix_repository_2():
    repo = RepoAsObject.from_directory(repo_path=repo_path)
    problems: RepoAsJson = repo.get_outputs_on_files(with_errors=True, with_outputs=False)

    if problems:
        print("❌ Trying and fix the problem")
        print(problems.convert_to_flat_txt())
        message = get_prompt_fix_repository(repo_name=repo_path.name)
        message += problems.convert_to_flat_txt()

def coucou_test_fixing_repo():
    from shutil import rmtree

    rmtree(TEST_PATH)
    create_empty_repo(TEST_PATH)

    repo = RepoAsObject.from_directory(repo_path=TEST_PATH)
    testing_repo = repo.get_outputs_on_files(with_errors=True, with_outputs=True)
    assert len(testing_repo.files) == 1
    fix_repository(repo_path=TEST_PATH)
    fix_repository(repo_path=TEST_PATH)
    repo = RepoAsObject.from_directory(repo_path=TEST_PATH)
    testing_repo = repo.get_outputs_on_files()
    assert testing_repo is None
    pass
    rmtree(TEST_PATH)
    create_empty_repo(TEST_PATH)
    
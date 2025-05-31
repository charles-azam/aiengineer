from aiengineer.testing import TESTING_PATH, TESTING_MODEL, initialise_empty_folder, initialise_folder_with_non_working_code, clean_after_test
import shutil
from pathlib import Path
from aider.repo import GitRepo

from aiengineer.tools.call_llm_on_repo import call_llm_on_repo, call_llm_on_repo_with_folder, fix_repository, call_llm_on_repo_with_files, RepoAsObject, RepoAsJson, get_repo_as_json_output, get_python_errors_in_repository, get_print_outputs_in_repository

def test_call_llm_on_repo():
    testing_dir = TESTING_PATH / "call_llm_on_repo"
    initialise_empty_folder(testing_dir)
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
    clean_after_test()
    
def test_call_llm_on_repo_with_files():
    testing_dir = TESTING_PATH / "call_llm_on_repo_with_files"
    initialise_empty_folder(testing_dir)
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
    clean_after_test()

    
def test_call_llm_on_repo_with_folder():
    testing_dir = TESTING_PATH / "call_llm_on_repo_with_folder"
    initialise_empty_folder(testing_dir)
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
    clean_after_test()
    
def test_fix_repository():
    initialise_folder_with_non_working_code()
    problems = fix_repository(repo_path=TESTING_PATH, litellm_id=TESTING_MODEL, edit_format="diff")
    problems = fix_repository(repo_path=TESTING_PATH, litellm_id=TESTING_MODEL, edit_format="diff")
    assert problems is None
    from testing.fix_repository.conversion import masse_g
    assert masse_g == 10000
    clean_after_test()
    
def test_get_repo_as_json_output():
    initialise_folder_with_non_working_code()
    repo_as_json = get_repo_as_json_output(with_errors=True, with_outputs=True, repo_path=TESTING_PATH)
    repo_as_dict = repo_as_json.to_dict()
    assert "10" in repo_as_dict["fix_repository/values.py"].content
    assert "No module named 'fix_repository'" in repo_as_dict["fix_repository/conversion.py"].content
    clean_after_test()
    
def test_get_python_errors_in_repository():
    initialise_folder_with_non_working_code()
    message = get_python_errors_in_repository(repo_path=TESTING_PATH)
    assert message.strip() == """

**fix_repository/values.py**: 
10


**fix_repository/conversion.py**: 
Error: Traceback (most recent call last):
  File "/Users/charlesazam/charloupioupiou/aiengineer/src/aiengineer/tools/parse_repository.py", line 234, in get_outputs_on_files
    spec.loader.exec_module(module)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/Users/charlesazam/charloupioupiou/aiengineer/src/testing/fix_repository/conversion.py", line 2, in <module>
    from fix_repository.values import masse_kg
ModuleNotFoundError: No module named \'fix_repository\'


""".strip()
    
    assert "10" in message
    assert "No module named 'fix_repository'" in message
    clean_after_test()
    
def test_get_print_outputs_in_repository():
    initialise_folder_with_non_working_code()
    message = get_print_outputs_in_repository(repo_path=TESTING_PATH)
    assert message.strip() == """

**fix_repository/values.py**: 
10
    """.strip()
    assert "10" in message
    assert "No module named 'fix_repository'" not in message
    clean_after_test()
    
    

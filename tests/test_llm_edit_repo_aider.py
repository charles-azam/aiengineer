import pytest

from aiengineer.testing import (TESTING_MODEL, TESTING_PATH, clean_after_test,
                                initialise_empty_folder,
                                initialise_folder_with_docs,
                                initialise_folder_with_non_working_code,
                                initialise_folder_with_working_code)

from aiengineer.aider_utils.llm_edit_repo import (
    llm_edit_repo,
    llm_edit_files,
    llm_edit_folder,
    llm_fix_repo,
)

def test_call_llm_on_repo():
    testing_dir = TESTING_PATH / "llm_edit_repo"
    initialise_empty_folder(testing_dir)
    llm_edit_repo(
        message="""
Create three files in a directory called llm_edit_repo:

1. **llm_edit_repo/a.py** – declare `a = 1`.  
2. **llm_edit_repo/b.py** – declare `b = 2`.  
3. **llm_edit_repo/c.py** –  
   • `import` `a` and `b`.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.

""",
        repo_path=TESTING_PATH,
        litellm_id=TESTING_MODEL,
    )
    from testing.llm_edit_repo import a, b, c
    from testing.llm_edit_repo.c import a, b, c

    assert c == 3
    clean_after_test()
    


def test_call_llm_on_repo_with_files():
    testing_dir = TESTING_PATH / "llm_edit_files"
    initialise_empty_folder(testing_dir)
    llm_edit_files(
        message="""
Create three files in a directory named llm_edit_files:

1. **llm_edit_folder/a.py** – declare `a = 1`.  
2. **llm_edit_folder/b.py** – declare `b = 2`.  
3. **llm_edit_folder/c.py** –  
   • `import` `a` and `b`.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.
4. **__init__.py** – create an empty file to make the directory importable.

""",
        fnames=[testing_dir / "a.py", testing_dir / "b.py", testing_dir / "c.py"],
        repo_path=TESTING_PATH,
        litellm_id=TESTING_MODEL,
    )
    from testing.llm_edit_files import a, b, c
    from testing.llm_edit_files.c import a, b, c

    assert c == 3
    clean_after_test()
    


def test_llm_edit_folder():
    testing_dir = TESTING_PATH / "llm_edit_folder"
    initialise_empty_folder(testing_dir)
    llm_edit_folder(
        message="""
Create three files in a directory named llm_edit_folder:

1. **llm_edit_folder/a.py** – declare `a = 1`.  
2. **llm_edit_folder/b.py** – declare `b = 2`.  
3. **llm_edit_folder/c.py** –  
   • `import` `a` and `b`.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.

""",
        folder_path=testing_dir,
        repo_path=TESTING_PATH,
        litellm_id=TESTING_MODEL,
    )
    from testing.llm_edit_folder import a, b, c
    from testing.llm_edit_folder.c import a, b, c

    assert c == 3
    clean_after_test()
    
@pytest.mark.strong_llm_only
def test_llm_fix_repo():
    initialise_folder_with_non_working_code()
    problems = llm_fix_repo(
        repo_path=TESTING_PATH, litellm_id=TESTING_MODEL, edit_format="diff"
    )
    problems = llm_fix_repo(
        repo_path=TESTING_PATH, litellm_id=TESTING_MODEL, edit_format="diff"
    )
    assert problems is None
    from testing.llm_fix_repo.conversion import masse_g

    assert masse_g == 10000
    clean_after_test()


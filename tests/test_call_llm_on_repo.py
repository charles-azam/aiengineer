from aiengineer.testing import TESTING_PATH, TESTING_MODEL
import shutil

from aiengineer.tools.call_llm_on_repo import call_llm_on_repo, fix_repository

def test_call_llm_on_repo():
    testing_dir = TESTING_PATH / "call_llm_on_repo"
    shutil.rmtree(testing_dir, ignore_errors=True)
    testing_dir.mkdir(parents=True, exist_ok=True)
    (testing_dir / "__init__.py").touch()
    
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
    

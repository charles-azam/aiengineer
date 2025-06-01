from pathlib import Path

import pytest
from aider.repo import GitRepo

from aiengineer.testing import (TESTING_MODEL, TESTING_PATH, clean_after_test,
                                initialise_empty_folder,
                                initialise_folder_with_docs,
                                initialise_folder_with_non_working_code,
                                initialise_folder_with_working_code)
from aiengineer.tools.call_llm_on_repo import (RepoAsJson, RepoAsObject,
                                               call_llm_on_repo,
                                               call_llm_on_repo_with_files,
                                               call_llm_on_repo_with_folder,
                                               fix_repository,
                                               get_print_outputs_in_repository,
                                               get_python_doc_as_markdown,
                                               get_python_errors_in_repository,
                                               get_repo_as_json_output,
                                               get_repository_map)


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
    problems = fix_repository(
        repo_path=TESTING_PATH, litellm_id=TESTING_MODEL, edit_format="diff"
    )
    problems = fix_repository(
        repo_path=TESTING_PATH, litellm_id=TESTING_MODEL, edit_format="diff"
    )
    assert problems is None
    from testing.fix_repository.conversion import masse_g

    assert masse_g == 10000
    clean_after_test()


def test_get_repo_as_json_output():
    initialise_folder_with_non_working_code()
    repo_as_json = get_repo_as_json_output(
        with_errors=True, with_outputs=True, repo_path=TESTING_PATH
    )
    repo_as_dict = repo_as_json.to_dict()
    assert "10" in repo_as_dict["fix_repository/values.py"].content
    assert (
        "No module named 'fix_repository'"
        in repo_as_dict["fix_repository/conversion.py"].content
    )
    clean_after_test()


def test_get_python_errors_in_repository():
    initialise_folder_with_non_working_code()
    message = get_python_errors_in_repository(repo_path=TESTING_PATH)
    assert (
        """**fix_repository/values.py**: 
10"""
        in message
    )
    assert "**fix_repository/conversion.py**: " in message
    assert "spec.loader.exec_module(module)" in message
    assert "No module named 'fix_repository'" in message
    clean_after_test()


def test_get_print_outputs_in_repository():
    initialise_folder_with_non_working_code()
    message = get_print_outputs_in_repository(repo_path=TESTING_PATH)
    assert (
        message.strip()
        == """

**fix_repository/values.py**: 
10
    """.strip()
    )
    assert "10" in message
    assert "No module named 'fix_repository'" not in message
    clean_after_test()


def test_get_repository_map():
    initialise_folder_with_working_code()
    repo_map = get_repository_map(repo_path=TESTING_PATH)
    assert (
        repo_map.strip()
        == """

**__init__.py**: 


**test_working_code/values.py**: 
Module Description:
Variables.

Variables:
masse_kg = 10

**test_working_code/conversion.py**: 
Module Description:
Conversion module for converting kg to pounds.

Functions:
def kg_to_pounds(kg_value):

**test_working_code/__init__.py**: 
""".strip()
    )
    pass
    clean_after_test()


def test_get_python_doc_as_markdown():
    doc_path = initialise_folder_with_docs()
    with pytest.raises(ValueError):
        markdown = get_python_doc_as_markdown(
            doc_path=doc_path / "coucou", repo_path=TESTING_PATH
        )

    markdown = get_python_doc_as_markdown(doc_path=doc_path, repo_path=TESTING_PATH)
    markdown_2 = get_python_doc_as_markdown(doc_path=doc_path, repo_path=TESTING_PATH)

    markdown_str = get_python_doc_as_markdown(
        doc_path="test_docs/docs.py", repo_path=TESTING_PATH
    )
    assert markdown_2 == markdown
    assert markdown_str == markdown

    assert (
        markdown.strip()
        == """

# Introduction
The system mass is 10 kg.


| Name    |   Age | City     |
|:--------|------:|:---------|
| Alice   |    25 | New York |
| Bob     |    30 | London   |
| Charlie |    35 | Paris    |

Sample data table
""".strip()
    )
    pass
    clean_after_test()

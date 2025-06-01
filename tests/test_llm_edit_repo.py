from pathlib import Path

import pytest
from aider.repo import GitRepo

from aiengineer.testing import (TESTING_MODEL, TESTING_PATH, clean_after_test,
                                initialise_empty_folder,
                                initialise_folder_with_docs,
                                initialise_folder_with_non_working_code,
                                initialise_folder_with_working_code)
from aiengineer.utils.llm_edit_repo import (
                                               llm_edit_repo,
                                               llm_edit_files,
                                               llm_edit_folder,
                                               llm_fix_repo,
                                               get_print_outputs_in_repository,
                                               get_python_doc_as_markdown,
                                               get_python_errors_and_print_outputs_in_repository,
                                               get_repo_as_json_output,
                                               get_repository_map)


def test_call_llm_on_repo():
    testing_dir = TESTING_PATH / "llm_edit_repo"
    initialise_empty_folder(testing_dir)
    llm_edit_repo(
        message="""
Create three files in a directory called llm_edit_repo:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b` using the `my_repo.` prefix.  
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
    from testing.llm_edit_folder import a, b, c
    from testing.llm_edit_folder.c import a, b, c

    assert c == 3
    clean_after_test()


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

@pytest.mark.no_api
def test_get_repo_as_json_output():
    initialise_folder_with_non_working_code()
    repo_as_json = get_repo_as_json_output(
        with_errors=True, with_outputs=True, repo_path=TESTING_PATH
    )
    repo_as_dict = repo_as_json.to_dict()
    assert "10" in repo_as_dict["llm_fix_repo/values.py"].content
    assert (
        "No module named 'llm_fix_repo'"
        in repo_as_dict["llm_fix_repo/conversion.py"].content
    )
    clean_after_test()

@pytest.mark.no_api
def test_get_python_errors_in_repository():
    initialise_folder_with_non_working_code()
    message = get_python_errors_and_print_outputs_in_repository(repo_path=TESTING_PATH)
    assert (
        """**llm_fix_repo/values.py**: 
10"""
        in message
    )
    assert "**llm_fix_repo/conversion.py**: " in message
    assert "spec.loader.exec_module(module)" in message
    assert "No module named 'llm_fix_repo'" in message
    clean_after_test()

@pytest.mark.no_api
def test_get_print_outputs_in_repository():
    initialise_folder_with_non_working_code()
    message = get_print_outputs_in_repository(repo_path=TESTING_PATH)
    assert (
        message.strip()
        == """

**llm_fix_repo/values.py**: 
10
    """.strip()
    )
    assert "10" in message
    assert "No module named 'llm_fix_repo'" not in message
    clean_after_test()

@pytest.mark.no_api
def test_get_repository_map_summary():
    initialise_folder_with_working_code()
    repo_map = get_repository_map(repo_path=TESTING_PATH, summary=True)
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

@pytest.mark.no_api
def test_get_repository_map():
    initialise_folder_with_working_code()
    repo_map = get_repository_map(repo_path=TESTING_PATH, summary=False)
    assert (
        repo_map.strip()
        == '''

**__init__.py**: 


**test_working_code/values.py**: 

"""Variables."""

masse_kg = 10
print(masse_kg)
    

**test_working_code/conversion.py**: 

"""Conversion module for converting kg to pounds."""

from testing.test_working_code.values import masse_kg

# Convert kg to pounds
def kg_to_pounds(kg_value):
    return kg_value * 2.20462

# Debug statement
print("DEBUG: conversion.py loaded successfully")
print(f"DEBUG: 1 kg = {kg_to_pounds(1)} pounds")
print(f"DEBUG: masse_kg ({masse_kg} kg) = {kg_to_pounds(masse_kg)} pounds")
    
    

**test_working_code/__init__.py**: 
'''.strip()
    )
    pass
    clean_after_test()

@pytest.mark.no_api
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

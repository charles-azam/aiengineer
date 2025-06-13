import pytest

from aiengineer.testing import (TESTING_MODEL, TESTING_PATH, clean_after_test,
                                initialise_empty_folder,
                                initialise_folder_with_docs,
                                initialise_folder_with_non_working_code,
                                initialise_folder_with_working_code)

from aiengineer.utils.llm_edit_repo import (
                                               get_print_outputs_in_repository,
                                               get_python_doc_as_markdown,
                                               get_python_errors_and_print_outputs_in_repository,
                                               get_repo_as_json_output,
                                               get_repository_map,
                                               exec_file_in_repo)


@pytest.mark.no_api
def test_get_repo_as_json_output():
    initialise_folder_with_non_working_code()
    repo_as_json = get_repo_as_json_output(
        with_errors=True, with_outputs=True, repo_path=TESTING_PATH
    )
    repo_as_dict = repo_as_json.to_dict()
    assert "10" in repo_as_dict["testing/llm_fix_repo/values.py"].content
    assert (
        "No module named 'llm_fix_repo'"
        in repo_as_dict["testing/llm_fix_repo/conversion.py"].content
    )
    clean_after_test()

@pytest.mark.no_api
def test_get_python_errors_in_repository():
    initialise_folder_with_non_working_code()
    message = get_python_errors_and_print_outputs_in_repository(repo_path=TESTING_PATH)
    assert (
        """**testing/llm_fix_repo/values.py**: 
10"""
        in message
    )
    assert "**testing/llm_fix_repo/conversion.py**: " in message
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

**testing/llm_fix_repo/values.py**: 
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

**testing/__init__.py**: 


**testing/test_working_code/__init__.py**: 


**testing/test_working_code/conversion.py**: 
Module Description:
Conversion module for converting kg to pounds.

Functions:
def kg_to_pounds(kg_value):

**testing/test_working_code/values.py**: 
Module Description:
Variables.

Variables:
masse_kg = 10
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

**testing/__init__.py**: 


**testing/test_working_code/__init__.py**: 


**testing/test_working_code/conversion.py**: 

"""Conversion module for converting kg to pounds."""

from testing.test_working_code.values import masse_kg

# Convert kg to pounds
def kg_to_pounds(kg_value):
    return kg_value * 2.20462

# Debug statement
print("DEBUG: conversion.py loaded successfully")
print(f"DEBUG: 1 kg = {kg_to_pounds(1)} pounds")
print(f"DEBUG: masse_kg ({masse_kg} kg) = {kg_to_pounds(masse_kg)} pounds")

**testing/test_working_code/values.py**: 

"""Variables."""

masse_kg = 10
print(masse_kg)
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
        doc_path="testing/test_docs/docs.py", repo_path=TESTING_PATH
    )
    assert markdown_2 == markdown
    assert markdown_str == markdown

    assert (
        markdown.strip()
        == """
---
title: Example PyForge Document
author: PyForge User
date: 2025-05-16

---





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


def test_exec_file_in_repo():
    initialise_folder_with_working_code()
    output = exec_file_in_repo(file_path="testing/test_working_code/conversion.py", repo_path=TESTING_PATH)
    assert "DEBUG: conversion.py loaded successfully" in output
    assert "DEBUG: 1 kg = 2.20462 pounds" in output
    assert "DEBUG: masse_kg (10 kg) = 22.0462 pounds" in output
    clean_after_test()
    
def test_exec_file_in_repo_with_error():
    initialise_folder_with_non_working_code()
    output = exec_file_in_repo(file_path="testing/llm_fix_repo/conversion.py", repo_path=TESTING_PATH)
    assert "No module named 'llm_fix_repo'" in output
    clean_after_test()
    

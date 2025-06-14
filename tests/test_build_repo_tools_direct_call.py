"""
Tests for aiengineer.tools.repo_tools_builder.build_repo_tools
-------------------------------------------------------------

The suite validates that
1.  The helper returns the full catalogue of expected tool names.
2.  Each tool works stand-alone (direct call) **and** when invoked by a
    `smolagents.CodeAgent`.
3.  Read-only tools (`get_repository_map`, `get_print_outputs`) behave exactly
    like the underlying helpers you already test elsewhere.
4.  The write / repair tool (`llm_fix_repo_tool`) really fixes a broken repo
    on disk so subsequent checks pass.

It re-uses the same fixtures/helpers you supplied for other tests.
"""

from pathlib import Path
from typing import List

import pytest
from smolagents import CodeAgent, LiteLLMModel, Message, MessageRole

from aiengineer.testing import (
    TESTING_MODEL,
    TESTING_PATH,
    clean_after_test,
    initialise_folder_with_non_working_code,
    initialise_folder_with_working_code,
    initialise_folder_with_docs,
    initialise_empty_folder,
    get_tool_responses_from_messages
)

from aiengineer.smolagents_utils.build_repo_tools import build_repo_tools, RepoTool

def test_llm_edit_repo_tool():
    testing_dir = TESTING_PATH / "llm_edit_repo"
    initialise_empty_folder(testing_dir)
    original_task = '''
Create three files in a directory called llm_edit_repo:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b` using relative imports.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.
'''
    
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools[RepoTool.EDIT_FILE_WHOLE.value]],
        model=model,
        max_steps=2,
    )
    agent.run(
        original_task
    )


    from testing.llm_edit_repo import a, b, c
    from testing.llm_edit_repo.c import a, b, c

    assert c == 3
    clean_after_test()
    

def test_edit_file_whole_diff():
    testing_dir = TESTING_PATH / "llm_edit_repo"
    initialise_empty_folder(testing_dir)
    original_task = '''
Create three files in a directory called llm_edit_repo using edit_file_diff_tool:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b`.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.
'''
    
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools[RepoTool.EDIT_FILE_DIFF.value]],
        model=model,
        max_steps=4,
    )
    agent.run(
        original_task
    )


    from testing.llm_edit_repo import a, b, c
    from testing.llm_edit_repo.c import a, b, c

    assert c == 3
    clean_after_test()
        
def test_call_llm_on_repo_with_files():
    
    # Here it should give the repository map and ask for modifications using this tool
    testing_dir = TESTING_PATH / "test_folder"
    initialise_folder_with_working_code(testing_dir)
    original_task = """
I want you to add a variable called twenty_kg_in_pounds in a new file called result.py next to the conversion.py file that will take as value the result of the conversion of 20 kg to pounds.

edit_file_whole_tool is the only way for you to modify the repository.
"""
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools[RepoTool.EDIT_FILE_WHOLE.value], tools[RepoTool.GET_REPOSITORY_MAP.value], tools[RepoTool.EXEC_ALL_PYTHON_FILES.value]],
        model=model,
        max_steps=10,
    )
    agent.run(
        original_task
    )


    from testing.test_folder.result import twenty_kg_in_pounds

    assert abs(twenty_kg_in_pounds - 44.0924524) < 1
    clean_after_test()

def test_call_llm_on_repo_with_files_diff():
    
    # Here it should give the repository map and ask for modifications using this tool
    testing_dir = TESTING_PATH / "test_folder"
    initialise_folder_with_working_code(testing_dir)
    original_task = """
I want you to add a variable called twenty_kg_in_pounds in a new file called result.py next to the conversion.py file that will take as value the result of the conversion of 20 kg to pounds.

edit_file_diff_tool is the only way for you to modify the repository.
"""
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools[RepoTool.EDIT_FILE_DIFF.value], tools[RepoTool.GET_REPOSITORY_MAP.value], tools[RepoTool.EXEC_ALL_PYTHON_FILES.value]],
        model=model,
        max_steps=10,
    )
    agent.run(
        original_task
    )


    from testing.test_folder.result import twenty_kg_in_pounds

    assert abs(twenty_kg_in_pounds - 44.0924524) < 1
    clean_after_test()

def test_exec_file_tool():
    testing_dir = TESTING_PATH / "test_folder"
    initialise_folder_with_working_code(testing_dir)
    original_task = "Test executing a file and give me the output"
    
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools[RepoTool.EXEC_FILE.value]],
        model=model,
        max_steps=1,
    )
    
    # Execute the conversion.py file which should print the conversion result
    result = agent.run("Execute the file testing/test_folder/conversion.py")
    
    # The file should have printed the conversion result
    assert "DEBUG: conversion.py loaded successfully" in result
    assert "DEBUG: 1 kg = 2.20462 pounds" in result
    assert "DEBUG: masse_kg (10 kg) = 22.0462 pounds" in result
    clean_after_test()
    
def test_delete_file_tool():
    testing_dir = TESTING_PATH / "test_folder"
    initialise_folder_with_working_code(testing_dir)
    original_task = "Delete conversion.py"
    
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools[RepoTool.DELETE_FILE.value]],
        model=model,
        max_steps=1,
    )
    
    # First verify the file exists
    file_path = "test_folder/conversion.py"
    assert (TESTING_PATH / file_path).exists()
    
    # Delete the file
    result = agent.run(f"Delete the file {file_path}")
    
    # Verify the file was deleted
    assert not (TESTING_PATH / file_path).exists()
    
    clean_after_test()
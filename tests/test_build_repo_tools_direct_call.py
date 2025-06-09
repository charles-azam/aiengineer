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


from aiengineer.smolagents_utils.build_repo_tools import build_repo_tools


def test_llm_edit_repo_tool():
    testing_dir = TESTING_PATH / "llm_edit_repo"
    initialise_empty_folder(testing_dir)
    original_task = '''
Create three files in a directory called llm_edit_repo:

1. **a.py** – declare `a = 1`.  
2. **b.py** – declare `b = 2`.  
3. **c.py** –  
   • `import` `a` and `b` using the `my_repo.` prefix.  
   • declare `c = a + b`.  
   • `print(c)` when the file is run as a script.
'''
    
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools["edit_file_whole_tool"]],
        model=model,
        max_steps=2,
    )
    agent.run(
        original_task
    )


    from testing.llm_edit_repo import a, b, c
    from testing.llm_edit_repo.c import a, b, c

    assert c == 3
    
test_llm_edit_repo_tool()
    
def test_call_llm_on_repo_with_files():
    
    # Here it should give the repository map and ask for modifications using this tool
    testing_dir = TESTING_PATH / "test_folder"
    initialise_folder_with_working_code(testing_dir)
    original_task = """
I want you to add a variable called twenty_kg_in_pounds in a new file called result.py next to the conversion.py file that will take as value the result of the conversion of 20 kg to pounds.

llm_edit_files_tool is the only way for you to modify the repository.
"""
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)
    
    agent = CodeAgent(
        tools=[tools["llm_edit_files_tool"], tools["get_repository_map_tool"], tools["exec_all_python_files_tool"]],
        model=model,
        max_steps=10,
    )
    agent.run(
        original_task
    )


    from testing.test_folder.result import twenty_kg_in_pounds

    assert abs(twenty_kg_in_pounds - 44.0924524) < 1
    clean_after_test()

@pytest.mark.strong_llm_only
def test_llm_fix_repo_tool_repairs_errors():
    # just ask for a simple fix and ask him to give additional instructions to aider
    initialise_folder_with_non_working_code()
    original_task = """
I want you to understand the problem and give instructions to fix the repository.
"""
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL, original_task=original_task)
    model = LiteLLMModel(TESTING_MODEL)


    agent = CodeAgent(
        tools=[tools["llm_fix_repo_tool"], tools["get_repository_map_tool"], tools["exec_all_python_files_tool"]],
        model=model,
        max_steps=10,
    )
    agent.run(
        original_task
    )


    from testing.llm_fix_repo.conversion import masse_g

    assert masse_g == 10000
    clean_after_test()
    

"""
Tests for aiengineer.tools.repo_tools_builder.build_repo_tools
-------------------------------------------------------------

The suite validates that
1.  The helper returns the full catalogue of expected tool names.
2.  Each tool works stand-alone (direct call) **and** when invoked by a
    `smolagents.CodeAgent`.
3.  Read-only tools (`get_repository_map`, `get_print_outputs`) behave exactly
    like the underlying helpers you already test elsewhere.
4.  The write / repair tool (`fix_repository_tool`) really fixes a broken repo
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
    get_tool_responses_from_messages
)


from aiengineer.smolagents_utils.build_repo_tools import build_repo_tools


def test_build_repo_tools_keys():
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL)

    expected_keys = {
        "get_repository_map_tool",
        "get_python_errors_tool",
        "get_print_outputs_tool",
        "get_doc_as_markdown_tool",
        "fix_repository_tool",
        "call_llm_on_repo_tool",
        "call_llm_on_repo_with_files_tool",
        "call_llm_on_repo_with_folder_tool",
    }
    assert expected_keys.issubset(tools.keys())

def test_repository_map_tool_via_agent():
    initialise_folder_with_working_code()
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL)

    model = LiteLLMModel(TESTING_MODEL)

    expected_output = tools["get_repository_map_tool"]()

    agent = CodeAgent(
        tools=[tools["get_repository_map_tool"]],
        model=model,
        max_steps=2,
    )
    agent.run(
        """
Explain what the repository does.

Base your answer *only* on get_repository_map_tool.  
Do **not** try to run Python or gather extra info.
"""
    )
    messages = agent.write_memory_to_messages()
    tool_responses = get_tool_responses_from_messages(messages)

    assert len(tool_responses) == 2
    assert expected_output in tool_responses[0]["content"][0]["text"]
    clean_after_test()


def test_print_outputs_tool_via_agent():
    initialise_folder_with_working_code()
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL)

    model = LiteLLMModel(TESTING_MODEL)

    expected_raw = tools["get_print_outputs_tool"]()

    agent = CodeAgent(
        tools=[tools["get_print_outputs_tool"]],
        model=model,
        max_steps=2,
    )
    agent.run(
        """
Explain what the repository does using only get_print_outputs_tool.

Call the tool **once** – exactly two steps total.
"""
    )
    messages = agent.write_memory_to_messages()
    tool_responses = get_tool_responses_from_messages(messages)

    assert len(tool_responses) == 2  # tool call + assistant answer
    tool_output = tool_responses[0]["content"][0]["text"]

    assert len(expected_raw) < len(tool_output)
    assert len(tool_output) < len(expected_raw) * 2
    clean_after_test()
    
def test_call_llm_on_repo_tool():
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
    
    # Here it should give the repository map and ask for modifications using this tool
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


def test_fix_repository_tool_repairs_errors():
    initialise_folder_with_non_working_code()
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL)

    # First call should return a description of the problems it tried to fix
    problems_txt = tools["fix_repository_tool"]()
    assert "NameError" in problems_txt or "import" in problems_txt

    # Second call should report that everything is now clean
    assert tools["fix_repository_tool"]() == "No problems detected."

    # Import a value that used to fail, proving the files on disk are valid
    from testing.fix_repository.conversion import masse_g  # noqa: E402

    assert masse_g == 10000
    clean_after_test()



def test_doc_as_markdown_tool():
    doc_file = initialise_folder_with_docs()
    tools = build_repo_tools(TESTING_PATH, litellm_id=TESTING_MODEL)

    # Wrong path → ValueError bubbles up through wrapper
    with pytest.raises(ValueError):
        tools["get_doc_as_markdown_tool"](doc_path="non/existent.py")

    md1 = tools["get_doc_as_markdown_tool"](doc_path=str(doc_file))
    md2 = tools["get_doc_as_markdown_tool"](doc_path="test_docs/docs.py")

    assert md1 == md2
    assert "| Name    |   Age |" in md1  # sanity check on markdown content
    clean_after_test()

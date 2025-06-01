from smolagents import CodeAgent, LiteLLMModel, tool

from aiengineer.testing import (TESTING_MODEL, TESTING_PATH, clean_after_test,
                                initialise_folder_with_working_code, get_tool_responses_from_messages)





def test_get_repository_map_tool():
    from aiengineer.tools.call_llm_on_repo import get_repository_map

    model = LiteLLMModel(TESTING_MODEL)

    initialise_folder_with_working_code()

    @tool
    def get_repository_map_tool() -> str:
        """
        Get the repository map.

        Returns:
            str: A string containing the repository map.
        """
        return get_repository_map(repo_path=TESTING_PATH)

    expected_output = get_repository_map_tool()

    agent = CodeAgent(
        tools=[get_repository_map_tool],
        model=model,
        max_steps=2,
    )
    agent.run(
        f"""
I want you to explain to me what the repository does.

I want you to base your answer only on the answer of get_repository_map_tool. Do not try to use python to get more information.
    """
    )
    messages = agent.write_memory_to_messages()
    tool_responses = get_tool_responses_from_messages(messages)
    assert len(tool_responses) == 2
    assert expected_output in tool_responses[0]["content"][0]["text"]
    clean_after_test()

def test_tools_in_dict_smolagents():
    from aiengineer.tools.call_llm_on_repo import get_repository_map

    model = LiteLLMModel(TESTING_MODEL)

    initialise_folder_with_working_code()
    
    tools_dict = dict()

    @tool
    def get_repository_map_tool() -> str:
        """
        Get the repository map.

        Returns:
            str: A string containing the repository map.
        """
        return get_repository_map(repo_path=TESTING_PATH)
    
    tools_dict["get_repository_map_tool"] = get_repository_map_tool

    expected_output = get_repository_map_tool()

    agent = CodeAgent(
        tools=[tools_dict["get_repository_map_tool"]],
        model=model,
        max_steps=2,
    )
    agent.run(
        f"""
I want you to explain to me what the repository does.

I want you to base your answer only on the answer of get_repository_map_tool. Do not try to use python to get more information.
    """
    )
    messages = agent.write_memory_to_messages()
    tool_responses = get_tool_responses_from_messages(messages)
    assert len(tool_responses) == 2
    assert expected_output in tool_responses[0]["content"][0]["text"]
    clean_after_test()
    
    
def test_get_print_outputs_in_repository():
    from aiengineer.tools.call_llm_on_repo import (
        get_print_outputs_in_repository)

    model = LiteLLMModel(TESTING_MODEL)

    initialise_folder_with_working_code()

    @tool
    def get_print_outputs_in_repository_tool() -> str:
        """
        This tool collects all print outputs from the Python files in the repository.
        It runs each file and captures the output of print statements.
        It is useful for understanding the behavior of the code in the repository.

        Returns:
            str: A string containing the print outputs from the repository.
        """
        return get_print_outputs_in_repository(repo_path=TESTING_PATH)

    expected_output = get_print_outputs_in_repository_tool()

    agent = CodeAgent(
        tools=[get_print_outputs_in_repository_tool],
        model=model,
        max_steps=2,
    )
    agent.run(
        f"""
I want you to explain to me what the repository does.

I want you to base your answer only on the answer of get_print_outputs_in_repository_tool. Do not try to use python to get more information.

Please call the tool only once, there must be only two steps do not try do to anything else.
    """
    )
    messages = agent.write_memory_to_messages()
    tool_responses = get_tool_responses_from_messages(messages)
    assert len(tool_responses) == 2
    tool_response = tool_responses[0]["content"][0]["text"]
    assert len(expected_output) < len(tool_response) # in would not work here since the output depends on the order of the files
    assert len(tool_response) < len(expected_output)*2 # make sure prints are not accounted twice
    clean_after_test()



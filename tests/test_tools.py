from smolagents import CodeAgent, LiteLLMModel, Message, MessageRole, tool

from aiengineer.testing import (TESTING_MODEL, TESTING_PATH, clean_after_test,
                                initialise_folder_with_working_code)


def get_tool_responses_from_messages(messages: list[Message]) -> list[Message]:
    return [
        message for message in messages if message["role"] == MessageRole.TOOL_RESPONSE
    ]


def test_get_repository_map_tool():
    from smolagents import CodeAgent, LiteLLMModel, tool

    from aiengineer.common import AIENGINEER_SRC_DIR

    REACTOR_PATH = AIENGINEER_SRC_DIR / "reactor"

    from aiengineer.tools.call_llm_on_repo import (
        get_print_outputs_in_repository, get_repository_map)

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

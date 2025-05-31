from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

register()
SmolagentsInstrumentor().instrument()

def test_get_all_print_outputs_in_repository():
    from smolagents import (
        CodeAgent,
        LiteLLMModel,
    )
    from smolagents import tool
    from aiengineer.tools.call_llm_on_repo import get_print_outputs_in_repository
    from aiengineer.testing import generate_testing_folder, TESTING_PATH, TESTING_MODEL

    model = LiteLLMModel(TESTING_MODEL)
    
    @tool
    def get_print_outputs_in_repository_tool() -> str:
        """
        Get all print outputs in the repository.

        Returns:
            str: A string containing all print outputs in the repository.
        """
        return get_print_outputs_in_repository(
            repo_path=TESTING_PATH,
        )
    

    agent = CodeAgent(
        tools=[get_print_outputs_in_repository_tool],
        model=model,
        max_steps=1,
    )
    output = agent.run("""
I want you to call get_print_outputs_in_repository_tool and tell what the answer.
    """)
    agent.logs
    
    
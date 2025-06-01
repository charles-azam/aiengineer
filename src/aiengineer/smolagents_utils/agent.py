from smolagents import (CodeAgent, InferenceClientModel, LiteLLMModel,
                        ToolCallingAgent, WebSearchTool, tool)

from aiengineer.smolagents_utils.tools import (
    ask_coder_fix_the_code_tool, ask_coder_modification_on_repo_tool,
    get_all_print_outputs_tool, get_codebase_as_markdown_tool)

model = LiteLLMModel("bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0")

manager_agent = CodeAgent(
    tools=[
        get_codebase_as_markdown_tool,
        ask_coder_fix_the_code_tool,
        ask_coder_modification_on_repo_tool,
        get_all_print_outputs_tool,
    ],
    model=model,
    additional_authorized_imports=["time", "numpy", "pandas"],
    max_steps=20,
)
if __name__ == "__main__":
    answer = manager_agent.run(
        """
Let's build a small modular reactor of around 20 MW to generate electricity.
We want a design that is as detailed as possible so that we know what to buy to our providers.
Our design must be cheap and easy to industrialize. We require at least three high-level systems: the reactor, the primary loop and the secondary loop.

You goal will be to use the tools to modify the codebase. You will act as a manager agent.

You can get access to the codebase as a markdown string using the tool get_codebase_as_markdown_tool.
Along with the outputs from the print statements in the codebase using the tool get_all_print_outputs_tool,
you can ask the agent to modify the codebase using the tool ask_coder_modification_on_repo_tool.

You

    """
    )

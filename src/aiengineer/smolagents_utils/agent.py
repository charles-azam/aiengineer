from smolagents import tool
from aiengineer.smolagents_utils.tools import ask_coder_fix_the_code_tool, ask_coder_modification_on_repo_tool, get_all_print_outputs_tool
from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    InferenceClientModel,
    WebSearchTool,
    LiteLLMModel,
)

model = LiteLLMModel("bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0") 

manager_agent = CodeAgent(
    tools=[ask_coder_fix_the_code_tool, ask_coder_modification_on_repo_tool, get_all_print_outputs_tool],
    model=model,
    additional_authorized_imports=["time", "numpy", "pandas"],
)
answer = manager_agent.run("If LLM training continues to scale up at the current rhythm until 2030, what would be the electric power in GW required to power the biggest training runs by 2030? What would that correspond to, compared to some countries? Please provide a source for any numbers used.")
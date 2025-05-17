from smolagents import (
    load_tool,
    CodeAgent,
    LiteLLMModel,
    GradioUI
)

# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

model = LiteLLMModel("bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0") 

# Initialize the agent with the image generation tool
agent = CodeAgent(tools=[image_generation_tool], model=model)

GradioUI(agent).launch()
from smolagents import CodeAgent, GradioUI, LiteLLMModel, load_tool

# Import tool from Hub
image_generation_tool = load_tool("m-ric/text-to-image", trust_remote_code=True)

model = LiteLLMModel("openai/gpt-4o")

# Initialize the agent with the image generation tool
agent = CodeAgent(tools=[image_generation_tool], model=model)

GradioUI(agent).launch()

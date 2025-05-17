from smolagents import CodeAgent, LiteLLMModel, WebSearchTool

model = LiteLLMModel("bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0") 

web_agent = CodeAgent(
    tools=[WebSearchTool()],
    model=model,
    name="web_search2",
    description="Runs web searches for you. Give it your query as an argument."
)

manager_agent = CodeAgent(
    tools=[], model=model, managed_agents=[web_agent]
)

manager_agent.run("Who is the CEO of Hugging Face?")
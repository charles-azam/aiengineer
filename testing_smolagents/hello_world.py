from smolagents import CodeAgent, AmazonBedrockServerModel, LiteLLMModel

model_id = LiteLLMModel("bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0") 

# you can also specify a particular provider e.g. provider="together" or provider="sambanova"
agent = CodeAgent(tools=[], model=model_id, add_base_tools=True)

agent.run(
    "Could you give me the 118th number in the Fibonacci sequence?",
)
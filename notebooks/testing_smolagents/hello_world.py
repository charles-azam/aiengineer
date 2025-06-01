from smolagents import AmazonBedrockServerModel, CodeAgent, LiteLLMModel

model_id = LiteLLMModel("openai/gpt-4o")

# you can also specify a particular provider e.g. provider="together" or provider="sambanova"
agent = CodeAgent(tools=[], model=model_id, add_base_tools=True)

agent.run(
    "Could you give me the 118th number in the Fibonacci sequence?",
)

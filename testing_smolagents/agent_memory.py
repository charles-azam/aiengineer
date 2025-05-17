from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel("bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0") 

agent = CodeAgent(tools=[], model=model, verbosity_level=0)

result = agent.run("What's the 20th Fibonacci number?")
agent.replay()
from smolagents import ActionStep

system_prompt_step = agent.memory.system_prompt
print("The system prompt given to the agent was:")
print(system_prompt_step.system_prompt)

task_step = agent.memory.steps[0]
print("\n\nThe first task step was:")
print(task_step.task)

for step in agent.memory.steps:
    if isinstance(step, ActionStep):
        if step.error is not None:
            print(f"\nStep {step.step_number} got this error:\n{step.error}\n")
        else:
            print(f"\nStep {step.step_number} got these observations:\n{step.observations}\n")
            
pass
from smolagents import ActionStep, CodeAgent, LiteLLMModel, TaskStep

model = LiteLLMModel("openai/gpt-4o")


agent = CodeAgent(tools=[], model=model, verbosity_level=1)
print(agent.memory.system_prompt)
agent.python_executor.send_tools({**agent.tools})
print(agent.memory.system_prompt)

task = "What is the 20th Fibonacci number?"

# You could modify the memory as needed here by inputting the memory of another agent.
# agent.memory.steps = previous_agent.memory.steps

# Let's start a new task!
agent.memory.steps.append(TaskStep(task=task, task_images=[]))

final_answer = None
step_number = 1
while final_answer is None and step_number <= 10:
    memory_step = ActionStep(
        step_number=step_number,
        observations_images=[],
    )
    # Run one step.
    final_answer = agent.step(memory_step)
    agent.memory.steps.append(memory_step)
    step_number += 1

    # Change the memory as you please!
    # For instance to update the latest step:
    # agent.memory.steps[-1] = ...

print("The final answer is:", final_answer)

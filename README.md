# AIEngineer – AI-Assisted Engineering Design Framework

Thank you for taking the time to explore this project!

My core belief is that engineering—especially systems engineering—should be performed through code. If you’re interested in the philosophy behind this approach, you can read my [manifest](https://charles-azam.github.io/documentation/manifest/).

Initially, my goal was to create a fully autonomous engineering agent. Very quickly, however, I realized that building such an agent would require a robust autonomous coding agent beneath it.

After experimenting extensively, I’ve settled on a two-package solution that has proven reliable and extensible:

- **Aider**  
  Aider excels at applying precise diffs to large repositories based on specific instructions. I tried to roll my own diffing logic, but Aider’s implementation (using diff format) is far more efficient and battle-tested. At first I tried using only aider in a for loop. Both of the approaches are implemented in this package.

- **smolagents**  
  I needed an agent framework to coordinate Aider. Many agent libraries introduce so much complexity that I end up reading and rewriting their core logic anyway. In contrast, Smolagents is intentionally lightweight. The codebase is small, the documentation is concise, and its abstractions genuinely accelerate development thanks to its focus on “coding agents.”

By combining Smolagents with Aider, I can have an AI-driven process that monitors repository changes, applies diffs, and incrementally builds out an “engineering object” in code. This setup allows the system to iterate, refactor, and expand itself without manual intervention—moving us toward a truly autonomous engineering workflow.

## Installation

This project is managed using the uv package manager.

For now, Pyforge is a submodule:

```bash
git clone --recurse-submodules https://github.com/charles-azam/aiengineer
uv sync
```

## Overview

AIEngineer creates a feedback loop between:
1. Engineering design specifications (in Python)
2. Simulation and validation
3. AI-driven design improvements

The framework is domain-agnostic and can be applied to various engineering fields including mechanical, electrical, chemical, and more.


## Examples

Examples can be found in `src/aiengineer/examples/`

I tried two different approaches, one with aider only in a for loop, the other with smolagents + aider.

## Usage

### Basic Usage

For `AIEngineer` to work, the root folder must be importable, that is why the reactor example is under `src/`.

Then, all it needs is a prompt !

```python
from aiengineer.config import EngineeringConfig
from aiengineer.common import AIENGINEER_SRC_DIR
from aiengineer.smolagents_utils.main_agent import create_smolagents_engineer

prompt_reactor = """
Design a modular high-temperature gas-cooled reactor (HTGR) system to decarbonizing industrial heat production. The system should:

    Utilize TRISO fuel particles and helium coolant, operating at core temperatures up to 600°C.

    Incorporate passive safety features, including heat removal and containment of fission products within fuel particles.

    Be modular and scalable, suitable for installation at various industrial sites.

    Provide thermal power outputs of 10, 15, or 20 MW, with a lifespan of 20 years and minimal refueling requirements.

    Ensure compatibility with existing industrial heat systems, delivering heat via a secondary CO2 loop to mediums such as steam, hot air, or thermal oil.

Additionally, outline the necessary infrastructure for manufacturing, assembly, and deployment, considering site requirements and regulatory compliance.
"""


CONFIG_REACTOR = EngineeringConfig(
    litellm_id="bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    iterations=200,
    repo_path=AIENGINEER_SRC_DIR / "reactor",
    prompt=prompt_reactor,
)


if __name__ == "__main__":
    smolagent_engineer, prompt = create_smolagents_engineer(CONFIG_REACTOR)

    smolagent_engineer.run(prompt)
    
```

### Project Structure

AIEngineer uses a convention-based file structure for engineering projects:

- `parameters_*.py` - Engineering parameters with units
- `systems_*.py` - System definitions and requirements
- `simulation_*.py` - Computations and physics models
- `tools_*.py` - Helper functions and utilities

## Testing

The pipeline only checks the tests that do not need an api.

To run all the test: `uv run pytest tests`


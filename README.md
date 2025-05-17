# AIEngineer - AI-Assisted Engineering Design Framework

AIEngineer is an open-source framework for iterative engineering design using large language models. It enables automated design iteration, simulation, and refinement for complex engineering projects.

## Overview

AIEngineer creates a feedback loop between:
1. Engineering design specifications (in Python)
2. Simulation and validation
3. AI-driven design improvements

The framework is domain-agnostic and can be applied to various engineering fields including mechanical, electrical, chemical, and more.

## Features

- Iterative design improvement through AI feedback loops
- Automatic error detection and correction
- Structured engineering project representation
- Customizable for different engineering domains
- Integration with various LLM providers

## Installation

This project is managed using the uv package manager.

For regular users:

```bash
uv sync
```

For development mode:

```bash
cd .. # parent folder to aiengineer
git clone https://github.com/charloupioupiou/pyforge.git
git clone https://github.com/Aider-AI/aider.git
git clone https://github.com/huggingface/smolagents.git
export DEV_MODE=1
```

## Usage

### Basic Usage

```python
from aiengineer.core import EngineeringProject
from aiengineer.config import EngineeringConfig

# Create a configuration
config = EngineeringConfig(
    domain="mechanical",
    model="bedrock/anthropic-claude-3-sonnet",
    iterations=10
)

# Initialize project
project = EngineeringProject(config)

# Run the iterative design process
project.run(prompt="Design a bridge with a 100m span...")
```

### Project Structure

AIEngineer uses a convention-based file structure for engineering projects:

- `parameters_*.py` - Engineering parameters with units
- `systems_*.py` - System definitions and requirements
- `simulation_*.py` - Computations and physics models
- `tools_*.py` - Helper functions and utilities

## Extending AIEngineer

### Custom Domains

Create domain-specific templates in the `domains/` directory:

```
domains/
  mechanical/
    templates/
      parameters_template.py
      systems_template.py
  electrical/
    templates/
      ...
```

### Custom LLM Providers

Implement the `LLMProvider` interface to add support for different LLM services.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



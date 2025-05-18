# AiEngineer

AIEngineer is an open-source framework for iterative engineering design using large language models. It enables automated design iteration, simulation, and refinement for complex engineering projects.

AIEngineer leverages the engineering-as-code library [Pyforge](https://charles-azam.github.io/documentation/Projects/Pyforge/)

Here is the documentation: [AIEngineer](https://charles-azam.github.io/documentation/Projects/AIEngineer/)

## Installation

This project is managed using the uv package manager.

For regular users:

```bash
git clone https://github.com/charles-azam/aiengineer
uv sync
```

For development mode:

```bash
cd .. # parent folder to aiengineer
git clone https://github.com/charles-azam/aiengineer
git clone https://github.com/charles-azam/pyforge.git
git clone https://github.com/Aider-AI/aider.git
git clone https://github.com/huggingface/smolagents.git
export DEV_MODE=1
```

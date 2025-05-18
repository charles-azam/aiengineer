# Contributing to AIEngineer

Thank you for your interest in contributing to AIEngineer! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment:
   ```bash
   cd .. # parent folder to aiengineer
   git clone https://github.com/charles-azam/pyforge.git
   git clone https://github.com/Aider-AI/aider.git
   git clone https://github.com/huggingface/smolagents.git
   export DEV_MODE=1
   cd aiengineer
   uv sync
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes, following the coding standards below

3. Write tests for your changes

4. Run the tests to ensure they pass:
   ```bash
   pytest
   ```

5. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

6. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a pull request on GitHub

## Coding Standards

- Follow PEP 8 style guidelines for Python code
- Include docstrings for all modules, classes, and functions
- Write clear, descriptive variable and function names
- Keep functions focused on a single responsibility
- Add type hints to function signatures

## Adding a New Domain

To add support for a new engineering domain:

1. Create a new directory under `src/aiengineer/domains/your_domain_name/`
2. Create a `template.py` file with domain-specific templates and configurations
3. Add an example prompt in `example_prompt.txt`
4. Update the documentation to mention the new domain

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting a pull request
- Include integration tests for complex features

## Documentation

- Update the README.md with any new features or changes
- Add or update docstrings for all public functions and classes
- Consider adding examples to demonstrate new functionality

## Submitting a Pull Request

1. Ensure your code passes all tests
2. Update the documentation as needed
3. Create a pull request with a clear description of the changes
4. Link any related issues in the pull request description

## License

By contributing to AIEngineer, you agree that your contributions will be licensed under the project's MIT license.

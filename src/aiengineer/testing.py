"""
Most software engineers would rather use fixtures instead of a simple testing file/folder.

But I can't help it, I hate fixtures. It is harder to debug And I find it hard to explain to beginners.
"""

import shutil
from pathlib import Path

from smolagents import Message, MessageRole

from aiengineer.common import AIENGINEER_SRC_DIR

TESTING_PATH = AIENGINEER_SRC_DIR / "testing"
TESTING_MODEL = "openai/gpt-4o"


def generate_testing_folder(testing_path: Path):
    """
    Generate a testing folder for the AI Engineer project.
    """
    if not testing_path.exists():
        testing_path.mkdir(parents=True, exist_ok=True)
    return testing_path


def initialise_empty_folder(folder_path: Path):
    shutil.rmtree(folder_path, ignore_errors=True)
    shutil.rmtree(folder_path.parent, ignore_errors=True)
    folder_path.mkdir(parents=True, exist_ok=True)
    (folder_path / "__init__.py").touch()
    (folder_path.parent / "__init__.py").touch()


def clean_after_test(testing_path: Path = TESTING_PATH):
    shutil.rmtree(testing_path, ignore_errors=True)
    testing_path.mkdir(parents=True, exist_ok=True)
    (testing_path / "__init__.py").touch()


def initialise_folder_with_non_working_code() -> Path:
    testing_dir = TESTING_PATH / "fix_repository"
    initialise_empty_folder(testing_dir)

    file = testing_dir / "conversion.py"
    file.write_text(
        """
from fix_repository.values import masse_kg

def convert_kg_to_g(a: float):
    return a * 100


masse_g = convert_kg_to_g(masse_kg)

assert masse_g*1000 == masse_kg       
    """
    )
    file = testing_dir / "values.py"
    file.write_text(
        """
masse_kg = 10
print(masse_kg)
    """
    )
    return testing_dir


def initialise_folder_with_working_code(
    testing_dir=TESTING_PATH / "test_working_code",
) -> Path:
    initialise_empty_folder(testing_dir)

    file = testing_dir / "conversion.py"
    file.write_text(
        '''
"""Conversion module for converting kg to pounds."""

from testing.{module_name}.values import masse_kg

# Convert kg to pounds
def kg_to_pounds(kg_value):
    return kg_value * 2.20462

# Debug statement
print("DEBUG: conversion.py loaded successfully")
print(f"DEBUG: 1 kg = {kg_to_pounds(1)} pounds")
print(f"DEBUG: masse_kg ({masse_kg} kg) = {kg_to_pounds(masse_kg)} pounds")
    
    '''.replace(
            "{module_name}", testing_dir.name
        )
    )
    file = testing_dir / "values.py"
    file.write_text(
        '''
"""Variables."""

masse_kg = 10
print(masse_kg)
    '''
    )
    return testing_dir


def initialise_folder_with_docs() -> Path:
    testing_dir = TESTING_PATH / "test_docs"
    initialise_folder_with_working_code(testing_dir)

    doc_path = testing_dir / "docs.py"
    doc_path.write_text(
        '''
"""Main document for the engineering project."""  

import pandas as pd
from testing.test_docs.values import masse_kg
from pyforge.note import (Citation, DocumentConfig, Figure, Reference, Table,
                          Title, display)

# Document configuration
config = DocumentConfig(
    title="Example PyForge Document", author="PyForge User", date="2025-05-16"
)
display(config)

# Create a sample dataframe for demonstration
df = pd.DataFrame(
    {
        "Name": ["Alice", "Bob", "Charlie"],
        "Age": [25, 30, 35],
        "City": ["New York", "London", "Paris"],
    }
)

display(
   f"""
# Introduction
The system mass is {masse_kg} kg.
""", Table(df, "Sample data table")
)

'''
    )
    return doc_path


def get_tool_responses_from_messages(messages: list[Message]) -> list[Message]:
    return [
        message for message in messages if message["role"] == MessageRole.TOOL_RESPONSE
    ]
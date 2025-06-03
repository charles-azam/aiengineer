from aiengineer.config import EngineeringConfig
from aiengineer.common import AIENGINEER_SRC_DIR
from aiengineer.smolagents_utils.main_agent import create_smolagents_engineer
from aiengineer.testing import initialise_empty_folder

prompt = """
I want you to find all the information you can on the EPYR startup and to try to create the design of their product
"""


CONFIG_EPYR = EngineeringConfig(
    litellm_id="openai/gpt-4o",
    iterations=20,
    repo_path=AIENGINEER_SRC_DIR / "epyr",
    prompt=prompt,
)


if __name__ == "__main__":
    smolagent_engineer, prompt = create_smolagents_engineer(CONFIG_EPYR)

    smolagent_engineer.run(prompt)
    
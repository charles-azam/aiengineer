"""
Example of using a simple for loop along with aider to build a nuclear reactor design project.
"""

from aiengineer.aider_utils.core import EngineeringProject
from aiengineer.aider_utils.prompts import get_prompt_ai_engineer
from aiengineer.common import AIENGINEER_SRC_DIR
from aiengineer.config import EngineeringConfig

PROMPT_REACTOR = """
Let's build a small modular reactor of around 20 MW to generate electricity.
We want a design that is as detailed as possible so that we know what to buy to our providers.
Our design must be cheap and easy to industrialize. We require at least three high-level systems: the reactor, the primary loop and the secondary loop.
"""


CONFIG_REACTOR = EngineeringConfig(
    litellm_id="bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    iterations=10,
    repo_path=AIENGINEER_SRC_DIR / "reactor",
    prompt=PROMPT_REACTOR,
)


project = EngineeringProject(
    config=CONFIG_REACTOR,
    system_prompt=get_prompt_ai_engineer(repo_name=CONFIG_REACTOR.repo_path.name),
)

if __name__ == "__main__":
    project.run()

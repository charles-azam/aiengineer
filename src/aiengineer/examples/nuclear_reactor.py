from aiengineer.config import EngineeringConfig
from aiengineer.common import AIENGINEER_SRC_DIR

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
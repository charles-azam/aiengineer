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
    litellm_id="openai/gpt-4o",
    iterations=100,
    repo_path=AIENGINEER_SRC_DIR / "reactor",
    prompt=prompt_reactor,
)


if __name__ == "__main__":
    smolagent_engineer, prompt = create_smolagents_engineer(CONFIG_REACTOR)

    smolagent_engineer.run(prompt)
    
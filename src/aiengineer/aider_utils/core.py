from pydantic import BaseModel

from aiengineer.config import EngineeringConfig
from aiengineer.aider_utils.engineer_agent import iterative_engineering_process


class EngineeringProject(BaseModel):
    config: EngineeringConfig
    system_prompt: str

    def run(self):
        iterative_engineering_process(
            repo_path=self.config.repo_path,
            question=self.config.prompt,
            system_prompt=self.system_prompt,
            litellm_id=self.config.litellm_id,
            iterations=self.config.iterations,
            trials=self.config.iterations,
        )

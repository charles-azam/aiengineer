from aiengineer.tools.engineer_agent import iterative_engineering_process
from aiengineer.config import EngineeringConfig
from pydantic import BaseModel

class EngineeringProject(BaseModel):
    config: EngineeringConfig
    system_prompt: str
    
    def run(self):
        iterative_engineering_process(repo_path=self.config.repo_path, question=self.config.prompt, system_prompt=self.system_prompt, litellm_id=self.config.litellm_id, iterations=self.config.iterations, trials=self.config.iterations)
    
    


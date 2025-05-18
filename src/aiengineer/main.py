from aiengineer.core import EngineeringProject
from aiengineer.template.nuclear_reactor import config
from aiengineer.prompts import get_prompt_ai_engineer

project = EngineeringProject(config=config, system_prompt=get_prompt_ai_engineer(repo_name=config.repo_path.name))

if __name__ == "__main__":
    project.run()
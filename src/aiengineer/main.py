from aiengineer.core import EngineeringProject
from aiengineer.template.nuclear_reactor import CONFIG_REACTOR
from aiengineer.prompts import get_prompt_ai_engineer

project = EngineeringProject(config=CONFIG_REACTOR, system_prompt=get_prompt_ai_engineer(repo_name=CONFIG_REACTOR.repo_path.name))

if __name__ == "__main__":
    project.run()
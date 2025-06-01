from pathlib import Path

from pydantic import BaseModel


class EngineeringConfig(BaseModel):
    litellm_id: str
    iterations: int
    repo_path: Path
    prompt: str

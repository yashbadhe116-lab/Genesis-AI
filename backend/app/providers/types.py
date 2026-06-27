from pydantic import BaseModel
from typing import Any, Dict

class AIRequest(BaseModel):
    prompt: str
    params: Dict[str, Any]

class AIResponse(BaseModel):
    provider_job_id: str
    status: str
    result_url: str | None = None

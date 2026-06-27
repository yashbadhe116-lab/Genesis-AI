from abc import ABC, abstractmethod
from app.providers.types import AIRequest, AIResponse, ProviderResult

class BaseProvider(ABC):
    @abstractmethod
    def generate(self, job: Any) -> ProviderResult:
        pass

    @abstractmethod
    def get_job_status(self, provider_job_id: str) -> str:
        pass

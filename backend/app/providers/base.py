from abc import ABC, abstractmethod
from app.providers.types import AIRequest, AIResponse

class BaseProvider(ABC):
    @abstractmethod
    def generate_image(self, request: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    def generate_video(self, request: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    def generate_audio(self, request: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    def generate_text(self, request: AIRequest) -> AIResponse:
        pass

    @abstractmethod
    def get_job_status(self, provider_job_id: str) -> str:
        pass

    @abstractmethod
    def cancel_job(self, provider_job_id: str) -> bool:
        pass

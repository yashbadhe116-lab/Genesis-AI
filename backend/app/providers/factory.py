from app.providers.base import BaseProvider
from app.providers.types import AIRequest, AIResponse

class MockProvider(BaseProvider):
    def __init__(self, name: str):
        self.name = name

    def generate_image(self, request: AIRequest) -> AIResponse:
        return AIResponse(provider_job_id=f"mock-{self.name}-1", status="processing")

    def generate_video(self, request: AIRequest) -> AIResponse:
        return AIResponse(provider_job_id=f"mock-{self.name}-1", status="processing")

    def generate_audio(self, request: AIRequest) -> AIResponse:
        return AIResponse(provider_job_id=f"mock-{self.name}-1", status="processing")

    def generate_text(self, request: AIRequest) -> AIResponse:
        return AIResponse(provider_job_id=f"mock-{self.name}-1", status="processing")

    def get_job_status(self, provider_job_id: str) -> str:
        return "processing"

    def cancel_job(self, provider_job_id: str) -> bool:
        return True

class ProviderFactory:
    _providers = {
        "openai": MockProvider("openai"),
        "google": MockProvider("google"),
        "runway": MockProvider("runway"),
        "kling": MockProvider("kling"),
        "elevenlabs": MockProvider("elevenlabs"),
        "stability": MockProvider("stability"),
    }

    @classmethod
    def get_provider(cls, name: str) -> BaseProvider:
        if name not in cls._providers:
            raise ValueError(f"Provider {name} not supported")
        return cls._providers[name]

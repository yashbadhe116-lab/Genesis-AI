import replicate
from app.providers.base import BaseProvider
from app.providers.types import AIRequest, AIResponse
from app.core.config import settings

class ReplicateProvider(BaseProvider):
    def __init__(self):
        self.client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
        self.model = settings.REPLICATE_MODEL_VERSION

    def generate_image(self, request: AIRequest) -> AIResponse:
        # Replicate typically takes prompt in input
        prediction = self.client.predictions.create(
            version=self.model,
            input={"prompt": request.prompt}
        )
        return AIResponse(provider_job_id=prediction.id, status=prediction.status)

    def generate_video(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError("Video generation not implemented for ReplicateProvider")

    def generate_audio(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError("Audio generation not implemented for ReplicateProvider")

    def generate_text(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError("Text generation not implemented for ReplicateProvider")

    def get_job_status(self, provider_job_id: str) -> str:
        prediction = self.client.predictions.get(provider_job_id)
        return prediction.status

    def cancel_job(self, provider_job_id: str) -> bool:
        self.client.predictions.cancel(provider_job_id)
        return True

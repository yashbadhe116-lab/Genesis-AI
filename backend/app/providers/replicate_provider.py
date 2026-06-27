import time
import replicate
import httpx
import logging
from app.providers.base import BaseProvider
from app.providers.types import ProviderResult
from app.core.config import settings

logger = logging.getLogger(__name__)

class ReplicateProvider(BaseProvider):
    def __init__(self):
        self.client = replicate.Client(api_token=settings.REPLICATE_API_TOKEN)
        self.model = settings.REPLICATE_MODEL_VERSION

    def generate(self, job: Any) -> ProviderResult:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                prediction = self.client.predictions.create(
                    version=self.model,
                    input={"prompt": job.input_data.get("prompt", "")}
                )
                logger.info(f"Replicate prediction created: {prediction.id}")
                
                # Manual polling to be safer
                while prediction.status not in ["succeeded", "failed", "canceled"]:
                    time.sleep(2)
                    prediction.reload()
                    logger.info(f"Prediction status: {prediction.status}")
                
                if prediction.status == "succeeded":
                    logger.info("Prediction succeeded")
                    return ProviderResult(
                        status="completed",
                        asset_type="image",
                        url=prediction.output,
                        metadata={"provider_job_id": prediction.id}
                    )
                else:
                    raise Exception(f"Provider failed with status: {prediction.status}")

            except Exception as e:
                logger.exception(f"Provider attempt {attempt} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
        
        raise Exception("Provider request failed")

    def get_job_status(self, provider_job_id: str) -> str:
        prediction = self.client.predictions.get(provider_job_id)
        return prediction.status

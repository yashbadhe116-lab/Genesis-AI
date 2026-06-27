import uuid
import requests
import logging
from pathlib import Path
from datetime import datetime

from app.infrastructure.redis import dequeue_job
from app.db.database import SessionLocal
from app.models.job import JobStatus
from app.providers.factory import ProviderFactory
from app.services import job_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

STORAGE_DIR = Path("generated_images")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)


def run_worker():
    logger.info("Worker started. Waiting for jobs...")

    while True:
        job_id = dequeue_job()
        logger.info(f"Job dequeued: {job_id}")

        with SessionLocal() as db:
            job = job_service.get_job(db, uuid.UUID(job_id))

            if not job:
                logger.error(f"Job {job_id} not found")
                continue

            job.status = JobStatus.PROCESSING
            db.commit()

            try:
                logger.info(f"Calling provider {job.provider_name} for job {job_id}")

                provider = ProviderFactory.get_provider(
                    job.provider_name or "replicate"
                )

                result = provider.generate(job)

                logger.info(f"Provider returned status: {result.status}")

                image_path = STORAGE_DIR / f"{job.id}.png"

                img_data = requests.get(result.url, timeout=30).content

                with open(image_path, "wb") as f:
                    f.write(img_data)

                logger.info(f"Saved image to {image_path}")

                # -------- SUCCESS --------
                job.status = JobStatus.COMPLETED
                job.progress = 100
                job.completed_at = datetime.utcnow()

                job.output_data = {
                    "url": result.url,
                    "local_path": str(image_path),
                    "public_url": f"/generated_images/{job.id}.png",
                    "metadata": result.metadata
                }

                logger.info(f"Database updated for completed job {job_id}")

            except Exception as e:
                logger.exception(f"Error processing job {job_id}: {e}")

                job.status = JobStatus.FAILED
                job.error_message = str(e)

            db.commit()

            logger.info(f"Job {job_id} finished with status {job.status}")


if __name__ == "__main__":
    run_worker()
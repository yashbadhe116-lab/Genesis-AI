import time
import uuid
from app.infrastructure.redis import dequeue_job
from app.db.database import SessionLocal
from app.models.job import JobStatus
from app.providers.factory import ProviderFactory
from app.services import job_service
from app.providers.types import AIRequest

def run_worker():
    print("Worker started. Waiting for jobs...")
    while True:
        job_id = dequeue_job()
        print(f"Processing job: {job_id}")
        
        with SessionLocal() as db:
            job = job_service.get_job(db, uuid.UUID(job_id))
            if not job:
                print(f"Job {job_id} not found")
                continue
            
            # Update status
            job.status = JobStatus.PROCESSING
            db.commit()
            
            # Get provider
            provider = ProviderFactory.get_provider(job.provider_name or "openai")
            
            # Call provider (mock)
            request = AIRequest(prompt=job.input_data.get("prompt", ""), params={})
            response = provider.generate_video(request)
            
            # Update status
            job.status = JobStatus.COMPLETED
            job.output_data = {"provider_job_id": response.provider_job_id}
            db.commit()
            print(f"Job {job_id} completed")

if __name__ == "__main__":
    run_worker()

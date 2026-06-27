import time
import uuid
import requests
import os
from pathlib import Path
from app.infrastructure.redis import dequeue_job
from app.db.database import SessionLocal
from app.models.job import JobStatus
from app.providers.factory import ProviderFactory
from app.services import job_service
from app.providers.types import AIRequest

STORAGE_DIR = Path("storage/images")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

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
            provider = ProviderFactory.get_provider(job.provider_name)
            
            # Initiate generation
            request = AIRequest(prompt=job.input_data.get("prompt", ""), params={})
            response = provider.generate_image(request)
            
            # Poll for completion
            provider_job_id = response.provider_job_id
            while True:
                status = provider.get_job_status(provider_job_id)
                if status == "succeeded":
                    # For Replicate, the output is in the prediction object
                    # Simplified for this structure:
                    prediction = provider.client.predictions.get(provider_job_id)
                    image_url = prediction.output[0]
                    
                    # Download image
                    image_path = STORAGE_DIR / f"{job.id}.png"
                    response_img = requests.get(image_url)
                    with open(image_path, "wb") as f:
                        f.write(response_img.content)
                    
                    job.status = JobStatus.COMPLETED
                    job.output_data = {"image_url": image_url, "local_path": str(image_path)}
                    break
                elif status in ["failed", "canceled"]:
                    job.status = JobStatus.FAILED
                    job.error_message = f"Provider job failed with status: {status}"
                    break
                time.sleep(2) # Poll every 2 seconds
                
            db.commit()
            print(f"Job {job_id} completed: {job.status}")

if __name__ == "__main__":
    run_worker()

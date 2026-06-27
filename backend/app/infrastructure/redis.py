import redis
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

JOB_QUEUE_NAME = "ai_jobs_queue"

def enqueue_job(job_id: str):
    redis_client.rpush(JOB_QUEUE_NAME, job_id)

def dequeue_job():
    # BLPOP blocks until a job is available
    _, job_id = redis_client.blpop(JOB_QUEUE_NAME)
    return job_id

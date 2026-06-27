#!/bin/bash
cd backend
export PYTHONPATH=$PYTHONPATH:.

# Start processes
python3 -m uvicorn main:app --port 8000 > server.log 2>&1 &
SERVER_PID=$!
python3 app/workers/job_worker.py > worker.log 2>&1 &
WORKER_PID=$!

echo "Processes started: Server($SERVER_PID), Worker($WORKER_PID)"
sleep 5

# 1. Login
response=$(curl -s -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=test@example.com&password=password123")
token=$(echo $response | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Token: $token"

# 2. Create Job
job_response=$(curl -s -X POST "http://127.0.0.1:8000/api/v1/jobs" \
     -H "Authorization: Bearer $token" \
     -H "Content-Type: application/json" \
     -d '{"job_type": "image_gen", "input_data": {"prompt": "a futuristic city"}, "provider_name": "replicate", "priority": 1}')
job_id=$(echo $job_response | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Job ID: $job_id"

# 3. Poll Status
for i in {1..20}; do
    status=$(curl -s -X GET "http://127.0.0.1:8000/api/v1/jobs/$job_id" \
         -H "Authorization: Bearer $token" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
    echo "Attempt $i - Status: $status"
    if [ "$status" == "COMPLETED" ] || [ "$status" == "FAILED" ]; then
        break
    fi
    sleep 5
done

# 4. Final verification
echo "Final Job Response:"
curl -s -X GET "http://127.0.0.1:8000/api/v1/jobs/$job_id" \
     -H "Authorization: Bearer $token"

# Cleanup
kill $SERVER_PID $WORKER_PID

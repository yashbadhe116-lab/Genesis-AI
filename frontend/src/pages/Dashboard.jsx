import AppLayout from "@/components/layout/AppLayout";
import { useState, useEffect } from 'react';
import api from '../api/api';

function Dashboard() {
  const [prompt, setPrompt] = useState('');
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(false);

  const generateImage = async () => {
    setLoading(true);
    try {
      const response = await api.post('/jobs', {
        job_type: 'image_gen',
        input_data: { prompt }
      });
      setJob(response.data);
    } catch (err) {
      alert('Error creating job');
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!job || job.status === 'completed' || job.status === 'failed') return;

    const interval = setInterval(async () => {
      try {
        const response = await api.get(`/jobs/${job.id}`);
        setJob(response.data);
        if (response.data.status === 'completed' || response.data.status === 'failed') {
          clearInterval(interval);
          setLoading(false);
        }
      } catch (err) {
        console.error('Error polling job', err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [job]);

  return (<AppLayout>
    <div style={{ padding: '20px' }}>
      <h1>Dashboard</h1>
      <input type="text" placeholder="Enter prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)} />
      <button onClick={generateImage} disabled={loading}>Generate</button>

      {job && (
        <div style={{ marginTop: '20px' }}>
          <p>Status: {job.status}</p>
          <p>Progress: {job.progress}%</p>

          {job.status === 'completed' && job.output_data && (
            <img
              src={`http://127.0.0.1:8000${job.output_data.public_url}`}
              alt="Generated"
              style={{ maxWidth: '100%', marginTop: '20px' }}
            />
          )}

          {job.status === 'failed' && <p style={{ color: 'red' }}>Error: {job.error_message}</p>}
        </div>
      )}
    </div>
  </AppLayout>
  )
    ;
}

export default Dashboard;

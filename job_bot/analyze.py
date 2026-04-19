import json
import requests
import os

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

def score_job(job: dict, resume: str) -> dict:
    prompt = f"""You are a career advisor. Given a resume and job description, return ONLY valid JSON with:
- fit_score: integer 0-100
- strengths: list of 2-3 matching skills
- gaps: list of 1-2 missing skills
- proceed: boolean (true if fit_score >= 65)

Resume:
{resume}

Job Title: {job['title']}
Job Description: {job['snippet']}

Return only JSON, no explanation."""

    response = requests.post(
        f'{OLLAMA_BASE_URL}/api/generate',
        json={
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'stream': False
        }
    )
    
    response.raise_for_status()
    raw = response.json()['response'].strip()
    return json.loads(raw)
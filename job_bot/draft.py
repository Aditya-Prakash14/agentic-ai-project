import requests
import os

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

def draft_cover_letter(job: dict, resume: str, analysis: dict) -> str:
    gaps_str = ", ".join(analysis.get("gaps", []))
    strengths_str = ", ".join(analysis.get("strengths", []))

    prompt = f"""Write a concise, genuine cover letter (3 short paragraphs, under 250 words).

Job: {job['title']}
Job Description: {job['snippet']}

Candidate strengths matching this role: {strengths_str}
Gaps to address honestly: {gaps_str}

Resume summary:
{resume[:1500]}

Rules:
- Do not start with "I am writing to..."
- Be specific, not generic
- Address one gap briefly and positively
- End with a clear call to action"""

    response = requests.post(
        f'{OLLAMA_BASE_URL}/api/generate',
        json={
            'model': OLLAMA_MODEL,
            'prompt': prompt,
            'stream': False
        }
    )
    
    response.raise_for_status()
    return response.json()['response'].strip()
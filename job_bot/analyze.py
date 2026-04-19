import json
import requests
import os

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

def score_job(job: dict, resume: str) -> dict:
    """Score a job using Ollama, with fallback if unavailable"""
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

    try:
        response = requests.post(
            f'{OLLAMA_BASE_URL}/api/generate',
            json={
                'model': OLLAMA_MODEL,
                'prompt': prompt,
                'stream': False
            },
            timeout=10
        )
        
        response.raise_for_status()
        raw = response.json()['response'].strip()
        return json.loads(raw)
    except Exception as e:
        # Fallback: simple keyword-based scoring
        print(f"Ollama unavailable ({str(e)}), using fallback scoring")
        return _fallback_score_job(job, resume)

def _fallback_score_job(job: dict, resume: str) -> dict:
    """Fallback scoring when Ollama is not available"""
    title_lower = job['title'].lower()
    snippet_lower = job.get('snippet', '').lower()
    resume_lower = resume.lower()
    job_text = f"{title_lower} {snippet_lower}"
    
    # Simple keyword matching
    tech_keywords = ['python', 'javascript', 'java', 'rust', 'go', 'react', 'django', 'fastapi']
    matching_tech = [k for k in tech_keywords if k in job_text and k in resume_lower]
    
    soft_keywords = ['communication', 'leadership', 'teamwork', 'problem-solving']
    matching_soft = [k for k in soft_keywords if k in job_text]
    
    # Calculate score
    base_score = 50
    if 'internship' in title_lower:
        base_score = 60
    if 'junior' in title_lower or 'entry' in title_lower:
        base_score = 65
    
    tech_boost = len(matching_tech) * 10
    soft_boost = len(matching_soft) * 5
    
    fit_score = min(100, base_score + tech_boost + soft_boost)
    
    return {
        "fit_score": fit_score,
        "strengths": matching_tech[:3] or ["strong technical foundation"],
        "gaps": ["specific project experience"] if fit_score < 80 else [],
        "proceed": fit_score >= 65
    }
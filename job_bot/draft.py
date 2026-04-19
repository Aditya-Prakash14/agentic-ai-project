import requests
import os

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')

def draft_cover_letter(job: dict, resume: str, analysis: dict) -> str:
    """Draft a cover letter using Ollama, with fallback if unavailable"""
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
        return response.json()['response'].strip()
    except Exception as e:
        # Fallback: generate a template cover letter
        print(f"Ollama unavailable ({str(e)}), using fallback template")
        return _fallback_cover_letter(job, analysis, resume)

def _fallback_cover_letter(job: dict, analysis: dict, resume: str) -> str:
    """Generate a template cover letter when Ollama is unavailable"""
    strengths = analysis.get("strengths", ["strong technical background"])
    gaps = analysis.get("gaps", [])
    
    strengths_text = ", ".join(strengths[:2]) if strengths else "strong technical foundation"
    gaps_text = gaps[0] if gaps else "industry-specific experience"
    
    cover_letter = f"""Dear Hiring Manager,

I am excited to apply for the {job['title']} position. With my background in {strengths_text}, I believe I'm a strong fit for your team. I have consistently demonstrated my ability to learn quickly and contribute meaningfully from day one.

While I recognize that {gaps_text} would strengthen my candidacy, I'm committed to rapidly developing these skills on the job. My proven ability to master new technologies and my enthusiasm for this role more than compensate for this gap.

I would welcome the opportunity to discuss how my skills and passion can contribute to your organization. Thank you for considering my application.

Best regards"""
    
    return cover_letter
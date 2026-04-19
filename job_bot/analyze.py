import json
import requests
import os

def score_job(job: dict, resume: str) -> dict:
    """Score a job using any available LLM API"""
    
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

    # Try Groq first (fastest & cheapest)
    if os.getenv("GROQ_API_KEY"):
        try:
            return _score_with_groq(prompt)
        except Exception as e:
            print(f"Groq error: {e}")
    
    # Try OpenRouter
    if os.getenv("OPENROUTER_API_KEY"):
        try:
            return _score_with_openrouter(prompt)
        except Exception as e:
            print(f"OpenRouter error: {e}")
    
    # Try OpenAI
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _score_with_openai(prompt)
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Try Anthropic Claude
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return _score_with_anthropic(prompt)
        except Exception as e:
            print(f"Anthropic error: {e}")
    
    # Try Google Gemini
    if os.getenv("GOOGLE_API_KEY"):
        try:
            return _score_with_google(prompt)
        except Exception as e:
            print(f"Google error: {e}")
    
    # Try Ollama
    if os.getenv("OLLAMA_BASE_URL"):
        try:
            return _score_with_ollama(prompt)
        except Exception as e:
            print(f"Ollama error: {e}")
    
    # Fallback
    print("No LLM API configured, using fallback scoring")
    return _fallback_score_job(job, resume)

def _score_with_groq(prompt: str) -> dict:
    """Use Groq API (fastest & cheapest)"""
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
    
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        timeout=10
    )
    
    text = response.choices[0].message.content.strip()
    return json.loads(text)

def _score_with_openrouter(prompt: str) -> dict:
    """Use OpenRouter API (multi-model)"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-70b-instruct")
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "Job Bot"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
        timeout=10
    )
    
    response.raise_for_status()
    text = response.json()['choices'][0]['message']['content'].strip()
    return json.loads(text)

def _score_with_openai(prompt: str) -> dict:
    """Use OpenAI API for job scoring"""
    import openai
    
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        timeout=10
    )
    
    text = response.choices[0].message.content.strip()
    return json.loads(text)

def _score_with_anthropic(prompt: str) -> dict:
    """Use Anthropic Claude API for job scoring"""
    import anthropic
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
        timeout=10
    )
    
    text = response.content[0].text.strip()
    return json.loads(text)

def _score_with_google(prompt: str) -> dict:
    """Use Google Gemini API for job scoring"""
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    
    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    response = model_obj.generate_content(prompt)
    
    text = response.text.strip()
    return json.loads(text)

def _score_with_ollama(prompt: str) -> dict:
    """Use local Ollama for job scoring"""
    base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'mistral')
    
    response = requests.post(
        f'{base_url}/api/generate',
        json={
            'model': model,
            'prompt': prompt,
            'stream': False
        },
        timeout=30
    )
    
    response.raise_for_status()
    raw = response.json()['response'].strip()
    return json.loads(raw)

def _fallback_score_job(job: dict, resume: str) -> dict:
    """Fallback scoring when no LLM is available"""
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
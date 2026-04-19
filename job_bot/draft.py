import requests
import os

def draft_cover_letter(job: dict, resume: str, analysis: dict) -> str:
    """Draft a cover letter using any available LLM API"""
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

    # Try Groq first (fastest & cheapest)
    if os.getenv("GROQ_API_KEY"):
        try:
            return _draft_with_groq(prompt)
        except Exception as e:
            print(f"Groq error: {e}")
    
    # Try OpenRouter
    if os.getenv("OPENROUTER_API_KEY"):
        try:
            return _draft_with_openrouter(prompt)
        except Exception as e:
            print(f"OpenRouter error: {e}")
    
    # Try OpenAI
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _draft_with_openai(prompt)
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Try Anthropic Claude
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            return _draft_with_anthropic(prompt)
        except Exception as e:
            print(f"Anthropic error: {e}")
    
    # Try Google Gemini
    if os.getenv("GOOGLE_API_KEY"):
        try:
            return _draft_with_google(prompt)
        except Exception as e:
            print(f"Google error: {e}")
    
    # Try Ollama
    if os.getenv("OLLAMA_BASE_URL"):
        try:
            return _draft_with_ollama(prompt)
        except Exception as e:
            print(f"Ollama error: {e}")
    
    # Fallback
    print("No LLM API configured, using fallback template")
    return _fallback_cover_letter(job, analysis, resume)

def _draft_with_groq(prompt: str) -> str:
    """Use Groq API for cover letter (fastest & cheapest)"""
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
    
    return response.choices[0].message.content.strip()

def _draft_with_openrouter(prompt: str) -> str:
    """Use OpenRouter API for cover letter"""
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
    return response.json()['choices'][0]['message']['content'].strip()

def _draft_with_openai(prompt: str) -> str:
    """Use OpenAI API for cover letter"""
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
    
    return response.choices[0].message.content.strip()

def _draft_with_anthropic(prompt: str) -> str:
    """Use Anthropic Claude API for cover letter"""
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
    
    return response.content[0].text.strip()

def _draft_with_google(prompt: str) -> str:
    """Use Google Gemini API for cover letter"""
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    model = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    
    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    response = model_obj.generate_content(prompt)
    
    return response.text.strip()

def _draft_with_ollama(prompt: str) -> str:
    """Use local Ollama for cover letter"""
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
    return response.json()['response'].strip()

def _fallback_cover_letter(job: dict, analysis: dict, resume: str) -> str:
    """Generate a template cover letter when no LLM is available"""
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
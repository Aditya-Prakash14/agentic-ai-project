"""
FastAPI backend for Job Bot frontend
Exposes REST API endpoints for job search, analysis, and application management
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
import asyncio
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search import search_jobs
from analyze import score_job
from draft import draft_cover_letter
from tracker import Tracker

app = FastAPI(title="Job Bot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

search_state = {
    "is_running": False,
    "progress": 0,
    "total": 0,
    "current_job": None,
    "status": "idle"
}

class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

class ConfigResponse(BaseModel):
    fit_score_threshold: int
    max_results: int
    enable_apply: bool
    auto_apply: bool

class LLMProvider(BaseModel):
    name: str
    display_name: str
    env_var: str
    requires_key: bool

class LLMConfigResponse(BaseModel):
    active_provider: str
    available_providers: List[dict]
    configured_providers: List[str]

class SetLLMProviderRequest(BaseModel):
    provider: str
    api_key: Optional[str] = None

class SearchProgress(BaseModel):
    is_running: bool
    progress: int
    total: int
    current_job: Optional[str]
    status: str

def load_resume():
    try:
        with open("resume.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="resume.txt not found")

def load_config():
    from dotenv import load_dotenv
    load_dotenv()
    return {
        "fit_score_threshold": int(os.getenv("FIT_SCORE_THRESHOLD", "65")),
        "max_results": int(os.getenv("MAX_RESULTS_PER_QUERY", "5")),
        "enable_apply": os.getenv("ENABLE_APPLY", "false").lower() == "true",
        "auto_apply": os.getenv("AUTO_APPLY", "false").lower() == "true"
    }

def get_available_llm_providers() -> dict:
    """Return available LLM providers and their configurations"""
    return {
        "openai": {
            "name": "openai",
            "display_name": "OpenAI (GPT-4/3.5)",
            "env_var": "OPENAI_API_KEY",
            "requires_key": True,
            "installed": _is_package_installed("openai")
        },
        "anthropic": {
            "name": "anthropic",
            "display_name": "Anthropic Claude",
            "env_var": "ANTHROPIC_API_KEY",
            "requires_key": True,
            "installed": _is_package_installed("anthropic")
        },
        "google": {
            "name": "google",
            "display_name": "Google Gemini",
            "env_var": "GOOGLE_API_KEY",
            "requires_key": True,
            "installed": _is_package_installed("google-generativeai")
        },
        "groq": {
            "name": "groq",
            "display_name": "Groq (Fast & Cheap)",
            "env_var": "GROQ_API_KEY",
            "requires_key": True,
            "installed": _is_package_installed("groq")
        },
        "openrouter": {
            "name": "openrouter",
            "display_name": "OpenRouter",
            "env_var": "OPENROUTER_API_KEY",
            "requires_key": True,
            "installed": True  # Uses requests, always available
        },
        "ollama": {
            "name": "ollama",
            "display_name": "Local Ollama",
            "env_var": None,
            "requires_key": False,
            "installed": True
        }
    }

def _is_package_installed(package_name: str) -> bool:
    """Check if a package is installed"""
    try:
        __import__(package_name.replace("-", "_"))
        return True
    except ImportError:
        return False

def get_active_llm_provider() -> str:
    """Get the currently active LLM provider from environment"""
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check priority order
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    elif os.getenv("ANTHROPIC_API_KEY"):
        return "anthropic"
    elif os.getenv("GOOGLE_API_KEY"):
        return "google"
    elif os.getenv("GROQ_API_KEY"):
        return "groq"
    elif os.getenv("OPENROUTER_API_KEY"):
        return "openrouter"
    else:
        return "ollama"  # Default to local Ollama

def get_tracker():
    return Tracker("tracker.json")

def generate_job_id(job: dict) -> str:
    import hashlib
    combined = f"{job['title']}{job['url']}"
    return hashlib.md5(combined.encode()).hexdigest()[:12]

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/api/config", response_model=ConfigResponse)
async def get_config():
    config = load_config()
    return config

@app.post("/api/search")
async def search(request: SearchRequest, background_tasks: BackgroundTasks):
    if search_state["is_running"]:
        raise HTTPException(status_code=409, detail="Search already in progress")
    background_tasks.add_task(run_search, request.query, request.num_results)
    return {
        "message": "Search started",
        "query": request.query,
        "status_url": "/api/search/progress"
    }

async def run_search(query: str, num_results: int):
    global search_state
    try:
        search_state["is_running"] = True
        search_state["status"] = "searching"
        search_state["current_job"] = "Searching..."
        search_state["progress"] = 0
        
        resume = load_resume()
        tracker = get_tracker()
        config = load_config()
        
        search_state["current_job"] = "Fetching job listings..."
        jobs = search_jobs(query, num=num_results)
        search_state["total"] = len(jobs)
        
        results = []
        for idx, job in enumerate(jobs):
            search_state["progress"] = idx + 1
            search_state["current_job"] = job["title"]
            
            job_id = generate_job_id(job)
            
            if tracker.has_seen(job_id):
                continue
            
            analysis = score_job(job, resume)
            score = analysis.get("fit_score", 0)
            
            cover_letter = None
            if analysis.get("proceed") and score >= config["fit_score_threshold"]:
                search_state["current_job"] = f"Drafting letter for {job['title']}"
                cover_letter = draft_cover_letter(job, resume, analysis)
            
            tracker.mark_seen(job_id)
            
            result = {
                "id": job_id,
                "title": job["title"],
                "url": job["url"],
                "snippet": job.get("snippet", ""),
                "fit_score": score,
                "strengths": analysis.get("strengths", []),
                "gaps": analysis.get("gaps", []),
                "timestamp": datetime.now().isoformat(),
                "cover_letter": cover_letter
            }
            results.append(result)
            tracker.add_result(result)
        
        search_state["status"] = "completed"
        search_state["current_job"] = f"Completed: {len(results)} jobs processed"
        
    except Exception as e:
        search_state["status"] = "error"
        search_state["current_job"] = f"Error: {str(e)}"
    finally:
        search_state["is_running"] = False

@app.get("/api/search/progress", response_model=SearchProgress)
async def get_search_progress():
    return search_state

@app.get("/api/results")
async def get_results(skip: int = 0, limit: int = 50):
    tracker = get_tracker()
    all_results = tracker.get_all()
    sorted_results = sorted(all_results, key=lambda x: x.get("timestamp", ""), reverse=True)
    return {
        "total": len(sorted_results),
        "results": sorted_results[skip:skip+limit]
    }

@app.get("/api/results/{job_id}")
async def get_result_detail(job_id: str):
    tracker = get_tracker()
    result = tracker.get_by_id(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result

@app.get("/api/results/{job_id}/cover-letter")
async def get_cover_letter(job_id: str):
    tracker = get_tracker()
    result = tracker.get_by_id(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    cover_letter = result.get("cover_letter")
    if not cover_letter:
        raise HTTPException(status_code=404, detail="No cover letter")
    return {"cover_letter": cover_letter}

@app.post("/api/results/{job_id}/apply")
async def apply_to_job(job_id: str):
    tracker = get_tracker()
    result = tracker.get_by_id(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    tracker.mark_applied(job_id)
    return {"message": "Job marked as applied", "id": job_id}

@app.delete("/api/results/{job_id}")
async def delete_result(job_id: str):
    tracker = get_tracker()
    tracker.delete(job_id)
    return {"message": "Result deleted", "id": job_id}

@app.get("/api/stats")
async def get_stats():
    tracker = get_tracker()
    all_results = tracker.get_all()
    applied = len([r for r in all_results if r.get("applied", False)])
    high_fit = len([r for r in all_results if r.get("fit_score", 0) >= 65])
    return {
        "total_jobs": len(all_results),
        "high_fit_jobs": high_fit,
        "applied": applied,
        "pending": high_fit - applied,
        "average_fit_score": sum(r.get("fit_score", 0) for r in all_results) / len(all_results) if all_results else 0
    }

@app.post("/api/reset")
async def reset_tracker():
    tracker = get_tracker()
    tracker.reset()
    return {"message": "Tracker reset"}

@app.get("/api/llm/config", response_model=LLMConfigResponse)
async def get_llm_config():
    """Get available LLM providers and active provider"""
    all_providers = get_available_llm_providers()
    active = get_active_llm_provider()
    
    configured = []
    for provider_name, provider_info in all_providers.items():
        if provider_info.get("env_var") and os.getenv(provider_info["env_var"]):
            configured.append(provider_name)
    
    return {
        "active_provider": active,
        "available_providers": [
            {
                "name": name,
                "display_name": info["display_name"],
                "requires_key": info["requires_key"],
                "installed": info["installed"]
            }
            for name, info in all_providers.items()
        ],
        "configured_providers": configured
    }

@app.post("/api/llm/set-provider")
async def set_llm_provider(request: SetLLMProviderRequest):
    """Set the active LLM provider"""
    from dotenv import load_dotenv
    
    all_providers = get_available_llm_providers()
    
    if request.provider not in all_providers:
        raise HTTPException(status_code=400, detail=f"Unknown provider: {request.provider}")
    
    provider_info = all_providers[request.provider]
    
    # Check if provider is installed
    if not provider_info["installed"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Provider '{request.provider}' is not installed. Run: pip install {request.provider}"
        )
    
    # Handle API key
    if provider_info["requires_key"]:
        if not request.api_key:
            raise HTTPException(
                status_code=400, 
                detail=f"Provider '{request.provider}' requires an API key"
            )
        
        # Update .env file
        env_var = provider_info["env_var"]
        _update_env_var(env_var, request.api_key)
        
        # Clear other provider keys
        for name, info in all_providers.items():
            if name != request.provider and info.get("env_var"):
                _update_env_var(info["env_var"], "")
    else:
        # Ollama - just clear other keys
        for name, info in all_providers.items():
            if name != "ollama" and info.get("env_var"):
                _update_env_var(info["env_var"], "")
    
    # Reload environment
    load_dotenv()
    
    return {
        "message": f"LLM provider set to {request.provider}",
        "provider": request.provider,
        "active_provider": get_active_llm_provider()
    }

def _update_env_var(var_name: str, value: str):
    """Update a variable in .env file"""
    env_file = ".env"
    
    # Read current .env
    lines = []
    var_found = False
    
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()
    
    # Update or add the variable
    new_lines = []
    for line in lines:
        if line.startswith(f"{var_name}="):
            var_found = True
            if value:
                new_lines.append(f"{var_name}={value}\n")
            # Skip line if value is empty (remove it)
        else:
            new_lines.append(line)
    
    if not var_found and value:
        new_lines.append(f"{var_name}={value}\n")
    
    # Write back
    with open(env_file, "w") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

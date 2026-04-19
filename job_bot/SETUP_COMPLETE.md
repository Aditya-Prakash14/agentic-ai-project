# Job Bot Complete Setup Guide

Complete guide to setting up Job Bot with multiple LLM provider support.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                  │
│  - Dashboard: View all jobs and statistics                  │
│  - Search: New job searches with progress tracking          │
│  - Job Detail: Individual job analysis and cover letters    │
│  - Settings: LLM provider configuration                     │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  - /api/search: Job search and analysis                     │
│  - /api/results: Job results management                     │
│  - /api/llm/*: LLM provider configuration                   │
│  - /api/config: Application settings                        │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   ┌────▼─────┐  ┌──────▼──────┐  ┌─────▼───────┐
   │   Groq   │  │ OpenAI/Claude│  │   Ollama    │
   │ (Fastest)│  │  (Best)      │  │  (Local)    │
   └──────────┘  └──────────────┘  └─────────────┘
```

## Prerequisites

- **Python 3.8+** (3.10+ recommended)
- **Node.js 16+** (18+ recommended)
- **Git**
- **pip** and **npm** package managers

## Installation Steps

### Step 1: Clone and Setup Project

```bash
# Navigate to project directory
cd ~/Documents/"agentic ai project"/job_bot

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your choices:
# Option A: Groq (recommended)
GROQ_API_KEY=your_groq_api_key

# Option B: OpenAI
OPENAI_API_KEY=your_openai_api_key

# Option C: Local Ollama (no API key needed)
# Just ensure Ollama is running

# Option D: Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key

# Other settings
FIT_SCORE_THRESHOLD=65
MAX_RESULTS_PER_QUERY=5
ENABLE_APPLY=false
AUTO_APPLY=false
```

### Step 3: Prepare Resume

```bash
# Create or place your resume in resume.txt
# This file will be used for job analysis and cover letter generation
echo "Your resume content here" > resume.txt
```

### Step 4: Start Services

#### Terminal 1 - Backend API

```bash
# Make sure you're in the project root
cd ~/Documents/"agentic ai project"/job_bot

# Activate virtual environment
source venv/bin/activate

# Start FastAPI backend
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2 - Frontend Development Server

```bash
# In a new terminal, navigate to frontend
cd ~/Documents/"agentic ai project"/job_bot/frontend

# Start development server
npm run dev
```

#### Terminal 3 (Optional) - Ollama (if using local)

```bash
# Only if using Ollama as LLM provider
ollama serve

# In another terminal, download a model:
ollama pull llama2  # or mistral, neural-chat
```

### Step 5: Access Application

Open browser and navigate to:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/docs (Swagger documentation)

## LLM Provider Setup

### Quick Setup Options

#### Option A: Groq (Recommended - 2 minutes)

1. Sign up at https://console.groq.com (free)
2. Get API key from https://console.groq.com/keys
3. Add to `.env`:
   ```
   GROQ_API_KEY=your_api_key
   ```
4. Restart backend
5. In Settings page, select Groq provider

Benefits:
- ⚡ Fastest inference
- 💰 Very affordable pricing
- 🎯 High accuracy
- 🚀 Production ready

#### Option B: Ollama (Free - 5 minutes)

1. Download from https://ollama.ai
2. Install and start:
   ```bash
   ollama serve
   ```
3. Download a model:
   ```bash
   ollama pull llama2  # or mistral, neural-chat
   ```
4. No API key needed - just set provider to "Local Ollama" in Settings

Benefits:
- 🆓 Completely free
- 🔒 100% privacy - runs locally
- 📱 No internet required
- 🎓 Good for learning

#### Option C: OpenAI (Best Quality - 2 minutes)

1. Sign up at https://platform.openai.com
2. Get API key from https://platform.openai.com/api-keys
3. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```
4. Restart backend

Benefits:
- ⭐ Best quality results
- 💪 Most capable model (GPT-4)
- 📊 Excellent documentation
- Note: Requires paid account

#### Option D: Switch Providers Later

You can change providers anytime:
1. Go to Settings → LLM Provider Configuration
2. Select new provider and enter API key
3. Click "Set Provider"
4. All new searches will use the new provider

See [LLM_PROVIDERS.md](LLM_PROVIDERS.md) for complete provider documentation.

## Usage Guide

### 1. Dashboard
- View all analyzed jobs
- See fit scores and statistics
- Track application status
- Quick access to cover letters

### 2. New Search
- Enter job search query
- Specify number of results
- Watch real-time progress
- Auto-analyze each job with fit score
- Generate cover letters for high-fit jobs

### 3. Job Detail
- View full job description
- See detailed fit analysis
- Read generated cover letter
- Mark as applied or delete

### 4. Settings
- Configure LLM provider
- Adjust fit score threshold
- View search configuration
- Manage API keys

## Project Structure

```
job_bot/
├── backend/
│   └── app.py              # FastAPI application with LLM endpoints
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Search.jsx
│   │   │   ├── JobDetail.jsx
│   │   │   └── Settings.jsx  # LLM provider configuration UI
│   │   └── services/
│   │       └── api.js      # API client with LLM endpoints
│   └── package.json
├── .env                     # Environment configuration
├── requirements.txt         # Python dependencies
├── LLM_PROVIDERS.md        # Complete LLM provider guide
├── search.py               # Job search functionality
├── analyze.py              # Job analysis with LLM
├── draft.py                # Cover letter generation
└── tracker.py              # Results tracking

```

## Key Features

### ✨ Multi-LLM Support
- Switch between Groq, OpenAI, Claude, Gemini, OpenRouter, Ollama
- Configure through intuitive Settings UI
- No restart required to switch providers

### 🔍 Smart Job Analysis
- Resume-based fit scoring (0-100)
- Strengths and gaps identification
- Automated cover letter generation
- Apply/skip recommendations

### 📊 Results Tracking
- Persistent job storage
- Application status tracking
- Statistics dashboard
- Export capabilities

### ⚡ Performance
- Real-time search progress
- Efficient LLM inference
- Responsive UI with React
- Background job processing

## API Endpoints

### Core Endpoints
- `GET /api/health` - Health check
- `GET /api/config` - Get application config
- `POST /api/search` - Start job search
- `GET /api/search/progress` - Get search progress

### Results Management
- `GET /api/results` - List all results
- `GET /api/results/{jobId}` - Get job detail
- `GET /api/results/{jobId}/cover-letter` - Get cover letter
- `POST /api/results/{jobId}/apply` - Mark as applied
- `DELETE /api/results/{jobId}` - Delete result

### LLM Configuration (NEW)
- `GET /api/llm/config` - Get available LLM providers
- `POST /api/llm/set-provider` - Set active LLM provider

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Try different port
python -m uvicorn backend.app:app --reload --port 8001
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf frontend/node_modules
cd frontend && npm install

# Try different port
npm run dev -- --port 3000
```

### LLM provider not working
1. Check API key is correct in Settings
2. Verify provider is installed: `pip list | grep [provider]`
3. Check backend logs for error messages
4. Try switching to Ollama as fallback

### Cover letters not generating
- Ensure resume.txt has content
- Check LLM provider is configured
- Try a different provider if current one fails
- Check backend logs for specific errors

### Connection refused errors
- Ensure backend is running on http://localhost:8000
- Ensure frontend is running on http://localhost:5173
- Check firewall settings
- Try restarting both services

## Performance Tips

1. **Use Groq**: Fastest and cheapest for production
2. **Enable Caching**: Avoid re-analyzing same jobs
3. **Batch Search**: Use reasonable result limits (5-20)
4. **Local Ollama**: Best for privacy-sensitive deployments
5. **Monitor Resources**: Check system resources for Ollama

## Security Considerations

1. **API Keys**: Keep API keys in `.env` file, not in git
2. **Resume Data**: Consider the privacy implications of using cloud LLMs
3. **HTTPS**: Use HTTPS in production
4. **Authentication**: Add auth layer for multi-user deployments
5. **Rate Limiting**: Implement rate limits for API endpoints

## Next Steps

1. ✅ Complete setup following this guide
2. ✅ Configure your preferred LLM provider
3. ✅ Add your resume to resume.txt
4. ✅ Test with a simple job search
5. ✅ Explore Settings to customize configuration
6. ✅ Read [LLM_PROVIDERS.md](LLM_PROVIDERS.md) for advanced options

## Support & Documentation

- **LLM Providers**: See [LLM_PROVIDERS.md](LLM_PROVIDERS.md)
- **API Documentation**: Visit http://localhost:8000/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **Backend README**: [BACKEND_README.md](BACKEND_README.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## Version Info

- Job Bot: 1.0.0
- FastAPI: 0.109.0+
- React: Latest
- Python: 3.8+
- Node: 16+

---

**Last Updated**: 2024
**Status**: ✅ Production Ready

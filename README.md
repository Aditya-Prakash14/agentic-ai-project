# Job Bot 🤖

An AI-powered job search, scoring, and cover letter pipeline that automates the low-value steps of job hunting so you can focus on interviews and networking.

## Features

✅ **Automated Job Search** — Search multiple job boards with custom queries  
✅ **AI Fit Scoring** — AI rates each job 0-100 based on your resume  
✅ **Smart Filtering** — Only draft cover letters for high-fit roles (≥65 by default)  
✅ **Cover Letter Generation** — Tailored 3-paragraph letters in seconds  
✅ **No Duplicates** — Tracker prevents reprocessing on subsequent runs  
✅ **Beautiful Dashboard** — Browse results with sortable fit scores  
✅ **Optional Submission** — Playwright automation for Easy Apply (disabled by default)  
✅ **🆕 Multi-LLM Support** — Groq, OpenAI, Claude, Gemini, OpenRouter, or local Ollama  
✅ **🆕 Web Interface** — Full React dashboard with real-time search progress  
✅ **🆕 Settings UI** — Configure LLM providers without restarting  

## 🆕 Multi-LLM Provider Support

Job Bot now supports **6 different LLM providers** with seamless switching:

### Quick Setup (Choose One)

#### 1️⃣ **Groq** (Recommended - 2 min setup)
- ⚡ **Fastest** inference (50-100ms)
- 💰 **Cheapest** ($0-10/month)
- 🎯 Excellent quality
- ✅ Free API key: https://console.groq.com

```bash
# Add to .env
GROQ_API_KEY=your_api_key
```

#### 2️⃣ **Ollama** (Free - Local Privacy)
- 🆓 **Completely free**, runs locally
- 🔒 **100% privacy**, no internet needed
- 📱 Works offline
- ✅ Download: https://ollama.ai

```bash
# No setup needed, just run:
ollama serve
ollama pull llama2
```

#### 3️⃣ **OpenAI** (Best Quality)
- ⭐ **Best quality** (GPT-4 available)
- 💪 Most capable model
- 💰 Moderate cost
- ✅ API key: https://platform.openai.com/api-keys

#### 4️⃣ **Claude** (Anthropic)
- ⭐ **Excellent quality** and reasoning
- 💰 Moderate cost
- ✅ API key: https://console.anthropic.com

#### 5️⃣ **Gemini** (Google)
- ⭐ **Good quality**, free tier available
- 💰 Cheap
- ✅ API key: https://makersuite.google.com/app/apikeys

#### 6️⃣ **OpenRouter** (Model Flexibility)
- 🔄 Access multiple models through one API
- 💰 Variable pricing
- ✅ API key: https://openrouter.ai

### Switch Providers Anytime

**No restart required!** Change providers through the web UI:

1. Open **Settings** → **LLM Provider Configuration**
2. Select your preferred provider
3. Enter API key (if needed)
4. Click **Set Provider**

All future searches will use the new provider immediately!

**See [LLM_PROVIDERS.md](LLM_PROVIDERS.md) for complete setup guide and [LLM_QUICK_REFERENCE.md](LLM_QUICK_REFERENCE.md) for quick start.**

---

## 🆕 Web Interface

### New React Dashboard

Beautiful, responsive web interface for managing your job search:

- **Dashboard** — View all jobs, fit scores, and statistics
- **Search** — New searches with real-time progress tracking
- **Job Detail** — Full analysis, cover letter, and application tracking
- **Settings** — Configure LLM providers and job search parameters

Start the interface:

```bash
# Terminal 1: Backend
python -m uvicorn backend.app:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Open http://localhost:5173
```

---

## ⚠️ Stage 4: Automated Applications

**Automated submission is DISABLED by default** for safety and compliance reasons:
- ⚠️ **Terms of Service Risk** — Job boards prohibit bot applications; use at your own risk
- ✅ **Manual Review** — Always review cover letters before submission
- ✅ **Opt-In Only** — You explicitly enable in `.env` before any submission happens

### Enable Stage 4 (If You Understand the Risks)

In `.env`:
```ini
ENABLE_APPLY=true          # Enable browser automation
AUTO_APPLY=false           # Require confirmation before each application (recommended)
```

Or for fully automated (⚠️ USE WITH EXTREME CAUTION):
```ini
ENABLE_APPLY=true
AUTO_APPLY=true            # Auto-submit without confirmation
```

### How It Works

When enabled, after drafting a cover letter, Job Bot will:
1. Open your browser to the job page
2. Find the "Easy Apply" button
3. Auto-fill the cover letter
4. **Prompt you to confirm** before submitting (if `AUTO_APPLY=false`)
5. Submit the application

### Disclaimer

By enabling Stage 4, you agree that:
- You are responsible for any Terms of Service violations
- You have read and accept the job board's automation policies
- Job Bot is provided AS-IS without warranties
- Always manually review your first few applications to ensure quality

## System Architecture

```
Stage 1: Search     → Find jobs via Serper API (Google search)
    ↓
Stage 2: Analyze    → Score fit against resume using Claude
    ↓
Stage 3: Draft      → Generate cover letters for high-fit roles
    ↓
Stage 4: Apply      → (Optional) Submit via browser automation
    ↓
Dashboard          → Browse results in beautiful HTML interface
```

## Setup

### 1. Clone & Install

```bash
git clone <repo>
cd job_bot
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install && cd ..

# If you want to use Stage 4 (automated applications), install Playwright browsers:
playwright install
```

### 2. Choose Your LLM Provider

**Easiest**: Ollama (free, local)
```bash
# Install from https://ollama.ai
ollama serve
ollama pull llama2  # or mistral, neural-chat
```

**Fastest**: Groq (recommended for production)
```bash
# Get free key: https://console.groq.com/keys
# Add to .env:
GROQ_API_KEY=your_api_key
```

**Best Quality**: OpenAI GPT-4
```bash
# Get API key: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-...
```

See [LLM_PROVIDERS.md](LLM_PROVIDERS.md) for all options.

### 3. Configure `.env`

```bash
cp .env.example .env
nano .env

# Add ONE of:
# GROQ_API_KEY=...          (recommended)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GOOGLE_API_KEY=...
# OPENROUTER_API_KEY=...
# (or leave all blank to use Ollama)

# Configure search
FIT_SCORE_THRESHOLD=65
MAX_RESULTS_PER_QUERY=5
```

### 4. Add Your Resume

```bash
# Edit resume.txt with your actual resume
nano resume.txt
```

### 5. Start Services

**Terminal 1 - Backend API:**
```bash
source venv/bin/activate  # if using venv
python -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Opens http://localhost:5173
```

**Terminal 3 - Ollama (if using Ollama):**
```bash
ollama serve
```

### 6. Access the Application

- **Web Dashboard**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs

---

## Old CLI Usage (Still Available)

For direct CLI pipeline (without web interface):

```bash
# 1. Add search queries to queries.txt (one per line)
# 2. Run pipeline
python main.py

# 3. View results
open dashboard.html  # macOS
```

But we recommend using the **web interface** for better experience!

## Configuration

### LLM Provider (.env)

Choose ONE provider:

```ini
# Option 1: Groq (RECOMMENDED)
GROQ_API_KEY=gsk_...

# Option 2: OpenAI
OPENAI_API_KEY=sk-...

# Option 3: Claude
ANTHROPIC_API_KEY=sk-ant-...

# Option 4: Google Gemini
GOOGLE_API_KEY=...

# Option 5: OpenRouter
OPENROUTER_API_KEY=...

# Option 6: Ollama (default, no key needed)
# Just ensure ollama serve is running
```

### Job Search Settings

```ini
FIT_SCORE_THRESHOLD=65          # Minimum score to draft cover letter
MAX_RESULTS_PER_QUERY=5         # Jobs per search query
```

### Application Settings (Advanced)

```ini
ENABLE_APPLY=false              # Enable Stage 4 (automated applications)
AUTO_APPLY=false                # Auto-submit without confirmation
```

**See [LLM_PROVIDERS.md](LLM_PROVIDERS.md) for detailed configuration guide.**

### Change Provider at Runtime

Use the **Settings** page in the web UI to switch LLM providers without restarting!

## File Structure

```
job_bot/
├── main.py              # Pipeline orchestrator
├── search.py            # Stage 1: Serper API integration
├── analyze.py           # Stage 2: Claude fit scoring
├── draft.py             # Stage 3: Cover letter generation
├── tracker.py           # Deduplication logic
├── dashboard.py         # HTML dashboard generator
├── resume.txt           # Your resume (plain text)
├── queries.txt          # Search queries (one per line)
├── .env                 # API keys (keep secret!)
├── tracker.json         # Auto-created: processed URLs
├── output/              # Auto-created: cover letter files
├── dashboard.html       # Auto-generated: results view
└── PRD.md              # Product requirements document
```

## Output Format

Cover letters are saved to `output/` with names like:

```
output/88_Backend_Internship.txt
output/72_Full_Stack_Engineer.txt
```

Each file contains:
- Job metadata (title, URL, fit score)
- Strengths & gaps analysis
- Full cover letter text

## Cost

### Free Options 🆓

**Ollama**: Completely free
- Runs locally on your machine
- No API costs, no rate limits
- **50-job run**: $0.00 (just electricity!)

### Cheap Options 💰

**Groq**: ~$0-10/month
- Free tier available
- Great performance
- **Recommended for production**

**Google Gemini**: Cheap
- Free tier with generous limits
- Low cost after free tier

### Premium Options 💰💰💰

**OpenAI**: $5-50+/month
- Best quality (GPT-4)
- $0.001-0.03 per request

**Claude**: $5-50+/month
- Excellent quality and reasoning
- $0.003-0.02 per request

## Cost Comparison

| Provider | Free? | Cost/Month | Speed | Quality |
|----------|-------|-----------|-------|---------|
| Ollama | ✅ Yes | $0 | Medium | Good |
| Groq | ✅ Tier | $0-10 | Very Fast | Good |
| Gemini | ✅ Tier | $0-5 | Fast | Good |
| Claude | ❌ | $10+ | Fast | Excellent |
| OpenAI | ❌ | $10+ | Fast | Excellent |

**Pro Tip**: Start with free Ollama, switch to Groq when ready for production! ⚡

## Rate Limiting

- 1-second delay between API calls to avoid throttling
- Serper free tier: 2,500 searches/month
- Anthropic: depends on your plan

## Tips for Best Results

1. **Resume quality** — Clear, well-formatted resume yields better scores
2. **Query specificity** — Use site: filters to target specific job boards
3. **Threshold tuning** — Lower threshold if too few matches, raise if too many
4. **Regular runs** — Schedule daily via cron or manually run each morning
5. **Review carefully** — AI-generated content should be reviewed before submission

## Future Enhancements

- [ ] Full job description extraction via Firecrawl
- [ ] Resume versioning with Pinecone/FAISS
- [ ] Email digest via SendGrid
- [ ] LangGraph orchestration for complex flows
- [ ] React dashboard UI
- [ ] ATS keyword optimization

## Troubleshooting

### Ollama connection error
Make sure Ollama is running: `ollama serve` (port 11434) or adjust `OLLAMA_BASE_URL` in `.env`

### Model not found
Pull the model first: `ollama pull mistral` (or your chosen model)

### Missing Serper API key
Add your API key to `.env`: `SERPER_API_KEY=your_key_here`

## Code Quality

This codebase is written to be readable by recruiters and interviewers as a portfolio piece. Key design principles:

- **Clear module separation** — Each stage is independent
- **Error handling** — Graceful failures with logging
- **No database** — Runs anywhere with Python
- **Legible output** — Self-contained HTML dashboard

## License

MIT

---

**Built with**: Python 3.11+ · Ollama (Local LLM) · Serper API · Playwright

Made with ❤️ for job seekers everywhere.

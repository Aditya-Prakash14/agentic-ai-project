# Job Bot 🤖

An AI-powered job search, scoring, and cover letter pipeline that automates the low-value steps of job hunting so you can focus on interviews and networking.

## Features

✅ **Automated Job Search** — Search multiple job boards with custom queries  
✅ **AI Fit Scoring** — Claude rates each job 0-100 based on your resume  
✅ **Smart Filtering** — Only draft cover letters for high-fit roles (≥65 by default)  
✅ **Cover Letter Generation** — Tailored 3-paragraph letters in seconds  
✅ **No Duplicates** — Tracker prevents reprocessing on subsequent runs  
✅ **Beautiful Dashboard** — Browse results with sortable fit scores  
✅ **Optional Submission** — Playwright automation for Easy Apply (disabled by default)  

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

# If you want to use Stage 4 (automated applications), install Playwright browsers:
playwright install
```

### 2. Set Up Ollama

- Install Ollama: https://ollama.ai
- Pull a model: `ollama pull mistral` (or `ollama pull neural-chat`, `ollama pull orca-mini`, etc.)
- Start Ollama server: `ollama serve` (runs on http://localhost:11434 by default)

### 3. Get API Keys

- **Serper**: https://google.serper.dev (Google Search API)

### 4. Configure `.env`

```bash
cp .env.example .env
# Edit .env and add your Serper API key and Ollama settings
nano .env
```

**Key settings:**
- `SERPER_API_KEY` — Your Serper API key
- `OLLAMA_BASE_URL` — Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL` — Model to use (default: mistral)
- `FIT_SCORE_THRESHOLD` — Minimum fit score to draft cover letters (default: 65)
- `MAX_RESULTS_PER_QUERY` — Jobs per search (default: 5)

### 5. Add Your Resume

Edit `resume.txt` with your actual resume in plain text.

### 6. Add Search Queries

Edit `queries.txt` with one search query per line:

```
software engineer internship 2025 site:linkedin.com
backend engineer new grad site:greenhouse.io
full stack developer internship site:lever.co
```

## Usage

### Run Pipeline

```bash
python main.py
```

This will:
1. Search for jobs matching each query in `queries.txt`
2. Score each job against your resume
3. Draft cover letters for high-fit matches (fit_score ≥ 65)
4. Generate `dashboard.html`

### View Results

```bash
open dashboard.html  # macOS
xdg-open dashboard.html  # Linux
start dashboard.html  # Windows
```

### Track Progress

Check `tracker.json` to see all processed URLs and their scores.

## Configuration

Edit `.env` to customize:

```ini
OLLAMA_BASE_URL=http://localhost:11434  # Your Ollama server
OLLAMA_MODEL=mistral                    # Model to use (mistral, neural-chat, orca-mini, etc.)
FIT_SCORE_THRESHOLD=65                  # Minimum score to draft cover letter
MAX_RESULTS_PER_QUERY=5                 # Jobs per search query
ENABLE_APPLY=false                      # Enable Stage 4 (automated applications) — DISABLED by default
AUTO_APPLY=false                        # If ENABLE_APPLY=true, auto-submit without confirmation
```

**Available Ollama models:**
- `mistral` — Fast, good quality (recommended)
- `neural-chat` — Optimized for conversations
- `orca-mini` — Lightweight, runs on low-end hardware
- `zephyr` — Fast and accurate
- See more: https://ollama.ai/library

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

**With Ollama: FREE!** 🎉

Ollama runs locally on your machine, so there are no API costs:
- Fit scoring: $0.00
- Cover letter generation: $0.00
- Total per job: $0.00

**50-job overnight run**: $0.00 (just your electricity costs!)

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

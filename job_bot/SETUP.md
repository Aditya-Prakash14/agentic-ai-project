# Job Bot Setup Guide

Complete setup instructions for getting the Job Bot running on your machine.

## Prerequisites

- **Python 3.8+** — [Download here](https://www.python.org)
- **Ollama** — Free local LLM runtime (instructions below)
- **Serper API Key** — Free tier available at [serper.dev](https://serper.dev)
- **Your Resume** — As plain text file (see below)

---

## 1. Clone & Install Dependencies

```bash
# Navigate to project directory
cd job_bot

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

---

## 2. Set Up Environment Variables

**IMPORTANT:** Environment variables contain sensitive API keys. Never commit `.env` to git!

```bash
# Copy the template file
cp .env.example .env

# Edit .env and add your credentials
# See: .env.example for what variables are needed
nano .env
```

### Required Variables

1. **SERPER_API_KEY** — Google search API
   - Sign up at [serper.dev](https://serper.dev)
   - Free tier: 100 searches/month
   - Copy your API key to `.env`

2. **OLLAMA_BASE_URL** — Local LLM endpoint
   - Default: `http://localhost:11434`
   - Only change if running Ollama on a different machine/port

3. **OLLAMA_MODEL** — Which model to use
   - Default: `mistral` (fast, good quality)
   - Other options: `neural-chat`, `llama2`, `dolphin-mixtral`

---

## 3. Install & Run Ollama

Ollama provides a **free, local LLM** with no API costs or data collection.

### macOS

```bash
# Option 1: Homebrew (recommended)
brew install ollama

# Option 2: Download directly
# https://ollama.ai/download/Ollama-darwin.zip
```

### Linux

```bash
curl https://ollama.ai/install.sh | sh
```

### Windows

Download installer: [ollama.ai/download](https://ollama.ai/download)

### Start Ollama

```bash
# Start the Ollama server (keep running in background)
ollama serve

# In a new terminal, pull the model (one-time setup)
ollama pull mistral
# OR for other models:
ollama pull neural-chat
```

**Ollama will listen on `http://localhost:11434`** — this is what Job Bot connects to.

---

## 4. Prepare Your Resume

Job Bot rates each job against your resume. Format it as plain text:

```bash
# Create resume.txt in the project root
cat > resume.txt << 'EOF'
Your Name
Email | Phone | LinkedIn

EDUCATION
University Name, B.S. Computer Science (2024)

EXPERIENCE
Software Engineer Intern, Company X (Summer 2023)
- Implemented feature using Python and Django
- Reduced query time by 40%

SKILLS
Languages: Python, JavaScript, Java
Frameworks: Django, React, FastAPI
Tools: Git, Docker, AWS
EOF
```

---

## 5. Verify Setup

```bash
# Verify all dependencies are installed
pip list | grep -E "requests|python-dotenv|playwright"

# Check that Ollama is running
curl http://localhost:11434/api/tags
# Should return a list of available models

# Test the main script (will search for "internship" and score jobs)
python main.py
```

---

## 6. (Optional) Enable Automated Applications

**⚠️ WARNING:** Automated submissions may violate job board Terms of Service. Use at your own risk!

To enable:

```bash
# In .env:
ENABLE_APPLY=true
AUTO_APPLY=false  # Recommended: require confirmation before each submission
```

Then Job Bot will:
1. Open your browser to each job
2. Auto-fill the cover letter
3. Prompt you to confirm before submitting
4. Submit the application

---

## Usage

### Search for a Single Query

```bash
python main.py
# Will search for "internship" (default) and process results
```

### Run Dashboard

```bash
python dashboard.py
# Opens http://localhost:8000 with all results and fit scores
```

### Track Applications

Job Bot automatically tracks which jobs it's already processed in `tracker.json`. To reset:

```bash
rm tracker.json
# Next run will reprocess all jobs
```

### Check Configuration

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('SERPER_API_KEY:', os.getenv('SERPER_API_KEY')[:10] + '***')"
```

---

## Troubleshooting

### "Connection refused" — Ollama not running

```bash
# Start Ollama in a new terminal
ollama serve

# Or check if it's already running
pgrep -i ollama
```

### "API key invalid" — Serper API issue

```bash
# Verify your API key is correct in .env
cat .env | grep SERPER_API_KEY

# Check rate limits at https://serper.dev/dashboard
```

### "Model not found" — Ollama model missing

```bash
# Download the model
ollama pull mistral

# List available models
ollama list
```

### ModuleNotFoundError — Missing dependencies

```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

---

## Project Structure

```
job_bot/
├── main.py                 # Entry point (orchestrates all stages)
├── search.py              # Stage 1: Search jobs via Serper API
├── analyze.py             # Stage 2: Score jobs with Claude/Ollama
├── draft.py               # Stage 3: Generate cover letters
├── apply.py               # Stage 4: Browser automation (optional)
├── dashboard.py           # View results in browser
├── tracker.py             # Deduplication logic
├── resume.txt             # Your resume (plain text)
├── requirements.txt       # Python dependencies
├── .env                   # Secrets (DO NOT COMMIT)
├── .env.example           # Template for .env
├── .gitignore             # Git ignore rules
├── SETUP.md              # This file
├── README.md             # Feature overview
├── PRD.md                # Product requirements
├── SECURITY.md           # Security best practices
└── output/               # Generated cover letters
```

---

## Next Steps

1. ✅ Complete setup above
2. 🔍 Run a test search: `python main.py`
3. 📊 View results: `python dashboard.py`
4. ✍️ Review generated cover letters in `output/` folder
5. 📤 (Optional) Enable `ENABLE_APPLY` and start submitting

---

## Support

- 🐛 Issue? Check `.env` is set up correctly
- 🤔 Questions? See README.md for feature overview
- ⚠️ Concerns? Read SECURITY.md for best practices

Enjoy automating your job search! 🚀

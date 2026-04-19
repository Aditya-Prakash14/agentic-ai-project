# Contributing to Job Bot

Guidelines for developing and improving Job Bot.

---

## Development Setup

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/job_bot.git
cd job_bot
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Set Up Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

---

## Code Style

### Python Standards

- **PEP 8**: Use standard Python formatting
- **Type hints**: Add type hints to function signatures
- **Docstrings**: Include docstrings for all functions

```python
def search_jobs(query: str, num: int = 5) -> list[dict]:
    """
    Search for jobs using Serper API.
    
    Args:
        query: Job search query (e.g., "Python internship")
        num: Number of results to return (default: 5)
    
    Returns:
        List of job postings with title, url, snippet
    """
    pass
```

### Comments & Documentation

- Write clear, concise comments
- Explain the "why", not the "what"
- Keep README.md and docs updated with changes

---

## Testing

Before submitting a PR:

```bash
# Run your changes
python main.py

# Test dashboard
python dashboard.py

# Check for syntax errors
python -m py_compile *.py
```

---

## Git Workflow

### Before Each Commit

```bash
# Verify .env is NOT being committed
git status | grep ".env"  # Should show nothing

# Check for secrets
git diff --cached | grep -i "api_key\|password"  # Should show nothing

# Safe to commit
git add .
git commit -m "Clear, descriptive message"
```

### Commit Message Format

```
[FEATURE/FIX/DOCS] Brief description

Optional longer explanation of what changed and why.
- Bullet point 1
- Bullet point 2

Fixes #123 (if applicable)
```

### Examples

```
[FEATURE] Add LinkedIn job scraper

Implemented a new module to search LinkedIn job postings.
Integrates with existing job ranking system.

- Added linkedin_search.py
- Updated search.py to call LinkedIn scraper
- Updated README with LinkedIn configuration

Fixes #45
```

---

## Pull Request Process

1. **Branch**: Create feature/fix branch from `main`
2. **Code**: Make changes following style guide
3. **Test**: Run `python main.py` and test your changes
4. **Document**: Update README/docs if needed
5. **Commit**: Clear, descriptive commits
6. **Push**: `git push origin your-branch`
7. **PR**: Open pull request with detailed description

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows PEP 8
- [ ] `.env` is NOT committed
- [ ] README/docs updated (if needed)
- [ ] Commit messages are clear
- [ ] No API keys or secrets exposed

---

## Architecture Overview

Job Bot follows a 4-stage pipeline:

```
Stage 1: Search    → search.py    (Find jobs)
     ↓
Stage 2: Analyze   → analyze.py   (Score fit)
     ↓
Stage 3: Draft     → draft.py     (Write letter)
     ↓
Stage 4: Apply     → apply.py     (Submit app)
```

Each stage:
- Takes clean input
- Produces clean output
- Can be tested independently
- Logs to stdout for debugging

### Module Contracts

**search_jobs()** → `list[dict]`
```python
{
    "title": "Software Engineer",
    "url": "https://...",
    "snippet": "We're hiring..."
}
```

**score_job()** → `dict`
```python
{
    "fit_score": 78,
    "proceed": True,
    "strengths": ["Python", "Django"],
    "gaps": ["Kubernetes"]
}
```

---

## Common Tasks

### Adding a New Job Source

1. Create `sources/linkedin.py` (or similar)
2. Implement `search_jobs(query: str, num: int) -> list[dict]`
3. Update `search.py` to call your new source
4. Update README with new source details
5. Test with `python main.py`

### Improving the Score Algorithm

1. Edit `analyze.py`
2. Test with sample jobs
3. Document scoring logic in code
4. Update PRD.md if needed

### Adding Configuration Options

1. Add to `.env.example`
2. Document in SETUP.md
3. Read from environment in code:
   ```python
   import os
   MY_SETTING = os.getenv('MY_SETTING', 'default_value')
   ```

---

## Reporting Issues

### Bug Report

```markdown
**Describe the bug:**
Cover letters aren't being generated

**Steps to reproduce:**
1. Run `python main.py`
2. See error: "ModuleNotFoundError: No module named 'claude'"

**Expected behavior:**
Should generate cover letter

**Environment:**
- OS: macOS 12
- Python: 3.9
- Ollama: Running
```

### Feature Request

```markdown
**Is your feature related to a problem?**
Job boards have different form requirements

**Describe the solution you'd like:**
Add support for LinkedIn's specific form fields

**Describe alternatives:**
Manual form filling (current state)
```

---

## Questions?

- Check README.md for feature overview
- See SETUP.md for troubleshooting
- Review SECURITY.md for secret handling
- Open an issue for questions or bugs

---

Happy contributing! 🚀

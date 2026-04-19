# PRODUCT REQUIREMENTS DOCUMENT

## Job Bot Agent

AI-powered job search, scoring, and cover letter pipeline

---

## 1. Overview

Job Bot is an autonomous agent that searches for internship and full-time job postings, scores each posting against a candidate's resume using an LLM, drafts tailored cover letters for high-fit roles, and (optionally) submits applications via browser automation. The system is designed to run overnight and surface a prioritised inbox of ready-to-submit applications each morning.

---

## 2. Problem Statement

Job searching at scale is time-consuming and repetitive. Candidates spend hours manually scanning job boards, copy-pasting descriptions into notes, and writing cover letters from scratch — the majority of which are for roles that are a poor fit. This project automates the low-value steps so the candidate can focus time on interviews and networking.

### Pain points addressed:
- Manual discovery — checking multiple job boards daily
- No systematic fit scoring — candidates apply to long-shot roles
- Generic cover letters — low response rates
- Repetitive form-filling — Easy Apply still takes 3–10 minutes per role

---

## 3. Goals & Non-Goals

### Goals
- Automate Stages 1–3 (search, score, draft) with no human input
- Produce fit-scored, cover-letter-ready results in a browsable HTML dashboard
- Avoid duplicate processing across runs via a persistent tracker
- Keep the codebase simple enough to demo to a recruiter in under 5 minutes

### Non-Goals
- Automated submission (Stage 4) is optional and disabled by default due to ToS risk
- The system does not maintain a user account or login session on job boards
- Resume parsing — the candidate provides resume.txt directly

---

## 4. Target Users

Primary: Computer science students and early-career software engineers applying to internships or new-grad roles. Secondary: Any job seeker comfortable running a Python script from the terminal.

---

## 5. System Architecture

The system is a four-stage linear pipeline orchestrated by a single Python entry point. Each stage is a standalone module with a clean input/output contract.

All processed URLs are written to tracker.json to prevent re-processing on subsequent runs. Output files are named with their fit score prefix (e.g. 88_Backend_Intern.txt) so they sort naturally by quality.

---

## 6. Functional Requirements

### 6.1 Stage 1 — Search
- Accepts a plain-text query (e.g. 'backend intern 2025 site:lever.co')
- Returns up to N results (configurable, default 5) with title, URL, and snippet
- Reads all queries from queries.txt and processes them in sequence
- Skips URLs already present in tracker.json

### 6.2 Stage 2 — Analyze
- Sends resume text and job snippet to Claude with a structured JSON prompt
- Response must include: fit_score (0–100), strengths (list), gaps (list), proceed (bool)
- proceed is true when fit_score >= 65 (configurable threshold)
- Handles JSON parse errors gracefully — logs and skips the job

### 6.3 Stage 3 — Draft
- Only invoked when proceed is true
- Generates a cover letter under 250 words in 3 paragraphs
- Prompt instructs the model to: reference specific strengths, address one gap honestly, avoid generic openers
- Saves output to /output/{score}_{title}.txt with metadata header

### 6.4 Stage 4 — Apply (Optional)
- Only invoked when `ENABLE_APPLY=true` in `.env`
- Uses Playwright to automate browser interaction
- Finds "Easy Apply" button on job posting
- Auto-fills cover letter in form fields
- Prompts user before submission (unless `AUTO_APPLY=true`)
- ⚠️ **Disabled by default** — User must opt-in explicitly due to ToS risk
- Logs success/failure of each submission attempt

### 6.5 Dashboard
- dashboard.py reads /output and tracker.json to build dashboard.html
- Cards sorted by fit_score descending
- Each card shows: title, URL, score, strength tags (green), gap tags (red), expandable cover letter
- Single static HTML file — no server required

### 6.6 Tracker
- tracker.json is created on first run and updated after each job is processed
- Schema: { url: { fit_score: int, proceeded: bool } }
- Prevents duplicate API calls across multiple runs

---

## 7. Tech Stack

| Component | Choice & rationale |
|---|---|
| Language | Python 3.11+ |
| LLM | Ollama (local, free, open-source models) |
| Job search | Serper API (google.serper.dev/search) |
| Browser automation | Playwright (Stage 4, optional) |
| Vector store | Pinecone or FAISS (future — resume versioning) |
| Config | python-dotenv (.env file) |
| Output | Plain text files + self-contained HTML dashboard |

---

## 8. Project File Structure

```
job_bot/
├── main.py          # Entry point — runs all queries
├── search.py        # Stage 1: Serper job search
├── analyze.py       # Stage 2: Ollama fit scoring
├── draft.py         # Stage 3: Ollama cover letter
├── apply.py         # Stage 4: Playwright browser automation (optional)
├── tracker.py       # Deduplication logic
├── dashboard.py     # HTML dashboard generator
├── resume.txt       # Candidate resume (plain text)
├── queries.txt      # One search query per line
├── tracker.json     # Auto-created — processed URL log
├── output/          # Generated cover letter files
└── .env             # SERPER_API_KEY, OLLAMA_BASE_URL, ENABLE_APPLY
```

---

## 9. Non-Functional Requirements

- **Rate limiting**: 1-second sleep between API calls to avoid throttling
- **Error handling**: each job processed in try/except; failures logged and skipped
- **Cost**: ~$0.01–0.03 per job processed (score + draft); 50-job overnight run ≈ $1
- **Portability**: no database, no server — runs on any machine with Python and npm
- **Legibility**: code should be readable by a recruiter or interviewer as a portfolio piece

---

## 10. Build Milestones

| Milestone | Done when... |
|---|---|
| M1 — Scoring | analyze.py reliably returns valid JSON for 10 test JDs |
| M2 — Search | search.py feeds real JDs from queries.txt into scoring |
| M3 — Draft | draft.py generates cover letters for all proceed=true results |
| M4 — Tracker | Re-running main.py skips already-processed URLs |
| M5 — Dashboard | dashboard.html renders all output cards correctly |
| M6 — Scheduler | cron job runs main.py + dashboard.py each morning (optional) |
| M7 — Stage 4 | Playwright fills Easy Apply forms for top matches (optional) |

---

## 11. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| ToS violations | Stage 4 disabled by default; user must opt in explicitly |
| LLM JSON errors | Wrapped in try/except; job skipped and logged on parse failure |
| Serper rate limits | 1s sleep between calls; Serper free tier: 2,500/month |
| Stale snippets | Snippets may not capture full JD — future: Firecrawl full-page fetch |
| Resume mismatch | Score threshold (65) is configurable — tune per candidate |

---

## 12. Future Work

- Firecrawl integration for full job description extraction (replace snippets)
- Pinecone / FAISS resume versioning — store multiple resume variants and select the best per role
- Email digest — send top 5 matches to inbox each morning via SendGrid
- LangGraph / CrewAI orchestration for more complex multi-agent planning
- Web UI — replace static HTML dashboard with a React front end
- ATS keyword injection — analyse job description for ATS keywords and surface gaps

---

## Appendix: Key Prompt Templates

### Scoring prompt (analyze.py)
Return ONLY valid JSON with: fit_score (0-100), strengths (list), gaps (list), proceed (bool, true if score >= 65). No preamble. Optimized for Ollama local models.

### Cover letter prompt (draft.py)
Write a 3-paragraph cover letter under 250 words. Do not start with "I am writing to...". Reference specific strengths, address one gap honestly, end with a clear call to action. Optimized for Ollama local models.

---

**Version**: 1.0  
**Date**: April 2026  
**Status**: Draft  
**Stack**: Python · Ollama · Serper · Playwright

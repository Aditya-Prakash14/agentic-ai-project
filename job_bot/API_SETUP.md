# Job Bot - LLM API Setup Guide

Job Bot works with **ANY** of these LLM providers. No Ollama needed!

## Quick Start

1. **Choose ONE provider** from below
2. **Get an API key** from that provider
3. **Add to `.env`** file
4. **Run the app** - it just works!

---

## 🚀 Option 1: OpenAI (Recommended for Beginners)

**Best for:** Free credits, easy setup, best quality

### Get Free API Key:

1. Go to https://platform.openai.com/signup
2. Sign up (free account)
3. Go to API keys: https://platform.openai.com/account/api-keys
4. Click "Create new secret key"
5. Copy the key

### Add to `.env`:

```bash
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini  # Fast & cheap
```

### Cost:
- **Free credits** ($5) on signup - enough to test!
- Then: ~$0.05 per job analyzed
- Max spend: Set in OpenAI dashboard

---

## 💬 Option 2: Anthropic Claude

**Best for:** Thoughtful analysis, good free tier

### Get API Key:

1. Go to https://console.anthropic.com/
2. Sign up (free account)
3. Create new API key
4. Copy it

### Add to `.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### Cost:
- Limited free tier
- Then: ~$0.10 per job analyzed

---

## 🔍 Option 3: Google Gemini (Free with Generous Limits)

**Best for:** Free usage, Google integration

### Get API Key:

1. Go to https://aistudio.google.com/apikey
2. Click "Get API key"
3. Create new API key
4. Copy it

### Add to `.env`:

```bash
GOOGLE_API_KEY=AIza-your-key-here
GOOGLE_MODEL=gemini-2.0-flash
```

### Cost:
- **Free**: 1000 requests/day, no credit card needed
- Excellent for testing

---

## 🖥️ Option 4: Local Ollama (No Cost, No API)

**Best for:** Privacy, zero cost, offline

### Setup:

1. Download Ollama: https://ollama.ai
2. Run: `ollama serve`
3. Pull a model:
   ```bash
   ollama pull mistral  # or llama2
   ```

### Add to `.env`:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

### Cost:
- **FREE** - all local
- Requires ~4GB RAM, ~10GB disk

---

## 📋 Configuration Checklist

- [ ] I have an API key from one provider
- [ ] I've added `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or configured Ollama
- [ ] I ran `pip install -r requirements.txt`
- [ ] I can run `./start.sh` without errors

---

## 🧪 Testing Your Setup

After configuring, test with:

```bash
cd job_bot
python -c "from analyze import score_job; print(score_job({'title': 'Test', 'snippet': 'Test job'}, 'Sample resume'))"
```

Should return JSON with fit_score.

---

## ⚡ Quick Commands

```bash
# Start everything
./start.sh

# Install dependencies
pip install -r requirements.txt
npm install --prefix frontend

# Open browser
open http://localhost:3000

# Test search
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "software engineer", "num_results": 3}'
```

---

## 💡 Which One to Choose?

| Provider | Cost | Setup | Quality | Best For |
|----------|------|-------|---------|----------|
| **OpenAI** | $$ Free credits | ⭐ Easy | ⭐⭐⭐ Best | Most users |
| **Anthropic** | $$ Free tier | ⭐⭐ Medium | ⭐⭐⭐ Great | Thoughtful analysis |
| **Google Gemini** | Free tier | ⭐ Easy | ⭐⭐ Good | Testing/free use |
| **Ollama** | Free | ⭐⭐⭐ Hard | ⭐⭐ Decent | Privacy-focused |

---

## 🆘 Troubleshooting

**"No LLM API configured"**
- Add one of the API keys to `.env`
- Restart the app: `./start.sh`

**"API key invalid"**
- Double-check your key is correct (copy paste carefully)
- Check API provider dashboard for active API

**"API is rate limited"**
- Free tier has limits. Set spending limit in provider dashboard
- Or switch to Ollama (local, unlimited)

**"Ollama not found"**
- Install it: https://ollama.ai
- Run: `ollama serve` in another terminal

---

## 🔒 Security Tips

- Never commit `.env` to git
- Use environment variables in production
- Rotate API keys regularly
- Set spending limits on cloud APIs

---

That's it! You're ready to go. Just add ONE API key and run! 🚀

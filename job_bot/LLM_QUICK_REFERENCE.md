# LLM Provider Quick Reference

## TL;DR - Get Started in 2 Minutes

### Groq (Recommended)
```bash
# 1. Get free API key: https://console.groq.com/keys
# 2. Add to .env:
GROQ_API_KEY=your_key_here

# 3. In Settings UI: Select Groq → Set Provider
# Done! ✅
```

### Ollama (Free, Local)
```bash
# 1. Install: https://ollama.ai
# 2. Run: ollama serve
# 3. In Settings UI: Select "Local Ollama" → Set Provider
# Done! ✅
```

### OpenAI
```bash
# 1. Get API key: https://platform.openai.com/api-keys
# 2. Add to .env:
OPENAI_API_KEY=sk-...

# 3. In Settings UI: Select OpenAI → Set Provider
# Done! ✅
```

---

## Provider Comparison

| | **Groq** | **Ollama** | **OpenAI** | **Claude** |
|---|----------|-----------|-----------|-----------|
| **Cost** | 💰 Cheap | 🆓 Free | 💰💰💰 | 💰💰💰 |
| **Speed** | ⚡⚡⚡ | ⚡⚡ | ⚡⚡ | ⚡⚡ |
| **Quality** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Setup** | 2 min | 5 min | 1 min | 1 min |
| **Privacy** | Cloud | 🔒 Local | Cloud | Cloud |
| **Best For** | Production | Privacy | Best Quality | Reliability |

---

## Environment Variables

### Groq
```
GROQ_API_KEY=gsk_xxxxxxxxxxxx
```

### OpenAI
```
OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

### Claude
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
```

### Gemini
```
GOOGLE_API_KEY=xxxxxxxxxxxx
```

### OpenRouter
```
OPENROUTER_API_KEY=xxxxxxxxxxxx
```

### Ollama
```
# No API key needed
OLLAMA_BASE_URL=http://localhost:11434
```

---

## Setup Commands

### Groq
```bash
# Get API key from https://console.groq.com/keys
echo "GROQ_API_KEY=your_key" >> .env
pip install groq
```

### Ollama
```bash
# Download from https://ollama.ai and install
ollama serve
# In another terminal:
ollama pull llama2
```

### OpenAI
```bash
# Get API key from https://platform.openai.com/api-keys
echo "OPENAI_API_KEY=sk-..." >> .env
pip install openai
```

### Claude
```bash
# Get API key from https://console.anthropic.com
echo "ANTHROPIC_API_KEY=sk-ant-..." >> .env
pip install anthropic
```

---

## Switch Provider Runtime

### Through Settings UI ✨ (Easiest)
1. Settings → LLM Provider Configuration
2. Select new provider
3. Enter API key (if needed)
4. Click "Set Provider"

### Through API
```bash
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "groq", "api_key": "gsk_..."}'
```

### Through Environment
```bash
# Edit .env and restart backend
# Remove old keys, add new one
nano .env
# Restart: Ctrl+C on backend, then run it again
```

---

## Cost Estimates (Monthly)

### Groq
- **$0-10/month** - Perfect for side projects
- Fast: ~50-100ms per request
- Free tier available

### Ollama
- **$0** - Completely free
- Slow: ~2-5 seconds per request
- Best for privacy

### OpenAI
- **$10-50+/month** - Depending on usage
- Fast: ~500-1000ms per request
- Best quality (GPT-4)

### Claude
- **$10-50+/month** - Depending on usage
- Fast: ~1-2 seconds per request
- Excellent for analysis

---

## Troubleshooting

### "Provider not installed"
```bash
pip install [provider-name]
# groq, openai, anthropic, google-generativeai
```

### "Invalid API key"
- Double-check the key in Settings
- Verify key hasn't expired/revoked
- Try generating a new key

### "Connection refused"
- Ensure backend is running: `python -m uvicorn backend.app:app --reload`
- Check port 8000 is available: `lsof -i :8000`
- Use different port if needed: `--port 8001`

### "Ollama not responding"
- Start Ollama: `ollama serve`
- Pull model: `ollama pull llama2`
- Check it's running: `curl http://localhost:11434/api/tags`

---

## Getting Free API Keys

### Groq ⭐
1. https://console.groq.com
2. Sign up (Google/Email)
3. Go to API Keys
4. Create new key
5. Copy it

**Free tier**: Generous limits, perfect for testing

### OpenAI
1. https://platform.openai.com
2. Sign up
3. Go to API keys
4. Create new secret key
5. **⚠️ Copy immediately** (won't show again)

**Note**: Requires credit card, but cheap

### Claude
1. https://console.anthropic.com
2. Sign up
3. Create API key
4. Copy it

**Free tier**: Limited, but available

### Gemini
1. https://makersuite.google.com/app/apikeys
2. Create API key
3. Select/create Google Cloud project
4. Copy

**Free tier**: Generous for learning

---

## Production Recommendations

### High Performance
→ Use **Groq** (fastest + cheapest)

### Best Quality
→ Use **OpenAI GPT-4** (best results)

### Privacy Critical
→ Use **Ollama** (local, no internet)

### Cost Conscious
→ Use **Groq** + **Ollama** (cheap + free)

### Mixed Setup
→ Use **Groq** for cover letters (fast) + **Ollama** fallback

---

## Monitor Usage

### Check API Logs
```bash
# Backend logs
tail -f job_bot.log
```

### View Active Provider
```bash
# Through API
curl http://localhost:8000/api/llm/config | jq

# Through frontend
Settings → LLM Provider Configuration
```

---

## Advanced: Custom Models with Ollama

```bash
# Pull specific model
ollama pull mistral
ollama pull neural-chat
ollama pull stable-code

# List available models
ollama list

# Configure in Job Bot
Settings → Local Ollama → Set Provider
# Will automatically use available model
```

---

## Quick Diagnostics

```bash
# Test if backend is running
curl http://localhost:8000/api/health

# Check LLM config
curl http://localhost:8000/api/llm/config | jq

# List installed packages
pip list | grep -E "groq|openai|anthropic|google"

# Check Ollama
curl http://localhost:11434/api/tags

# Check active provider
curl http://localhost:8000/api/config | jq
```

---

## Need Help?

1. **Settings UI** - Use this first, easiest to debug
2. **Backend logs** - Check error messages
3. **LLM_PROVIDERS.md** - Full documentation
4. **API docs** - http://localhost:8000/docs

---

**Pro Tip**: Start with Ollama (free, local), then switch to Groq when ready for production! 🚀

# LLM Provider Configuration Guide

Job Bot supports multiple LLM providers for AI-powered job analysis and cover letter generation. You can switch between providers at any time through the Settings page in the frontend or by configuring environment variables.

## Quick Start

### Option 1: Groq (Recommended) ⭐ 
Fast, cheap, and easy to set up.

```bash
# 1. Sign up at https://console.groq.com
# 2. Get your API key from https://console.groq.com/keys
# 3. Add to .env file:
GROQ_API_KEY=your_api_key_here

# 4. Install package (if not already installed)
pip install groq

# 5. Set as active provider:
# Option A: Through frontend Settings > LLM Provider Configuration > Select Groq > Set Provider
# Option B: Through API:
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "groq", "api_key": "your_api_key"}'
```

### Option 2: Local Ollama (Free, No API Key)
Run LLMs locally on your machine.

```bash
# 1. Install Ollama from https://ollama.ai
# 2. Start Ollama service:
ollama serve

# 3. Download a model (in another terminal):
ollama pull llama2  # or mistral, neural-chat, etc.

# 4. Set as active provider:
# Through frontend Settings > Select "Local Ollama" > Set Provider
```

### Option 3: OpenAI (GPT-4/3.5)
Use OpenAI's powerful models.

```bash
# 1. Sign up at https://openai.com
# 2. Get API key from https://platform.openai.com/api-keys
# 3. Add to .env file:
OPENAI_API_KEY=sk-...

# 4. Install package:
pip install openai

# 5. Set as active provider through Settings
```

### Option 4: Anthropic Claude
Use Claude for analysis.

```bash
# 1. Sign up at https://console.anthropic.com
# 2. Get API key from account settings
# 3. Add to .env file:
ANTHROPIC_API_KEY=sk-ant-...

# 4. Install package:
pip install anthropic

# 5. Set as active provider through Settings
```

### Option 5: Google Gemini
Use Google's Gemini models.

```bash
# 1. Sign up at https://makersuite.google.com/app/apikeys
# 2. Create API key
# 3. Add to .env file:
GOOGLE_API_KEY=your_api_key_here

# 4. Install package:
pip install google-generativeai

# 5. Set as active provider through Settings
```

### Option 6: OpenRouter
Access multiple models through one API.

```bash
# 1. Sign up at https://openrouter.ai
# 2. Get API key from dashboard
# 3. Add to .env file:
OPENROUTER_API_KEY=your_api_key_here

# 4. No additional installation needed (uses requests)

# 5. Set as active provider through Settings
```

## Web Interface

### Via Settings Page

1. **Navigate to Settings** in the Job Bot dashboard
2. **LLM Provider Configuration** section shows:
   - ✅ Currently active provider
   - Available providers with installation status
   - Configured providers (those with API keys set)

3. **Select a provider**:
   - Click on the provider card to select it
   - For non-local providers, enter your API key
   - Click "Set Provider"

### Features

- **Installation Detection**: Shows which providers are installed on your system
- **Configuration Status**: Indicates if a provider already has an API key configured
- **Automatic Provider Switching**: Seamlessly switch between providers without restarting
- **Safe Defaults**: Falls back to Ollama if no external provider is configured

## API Reference

### Get Available Providers

```bash
GET /api/llm/config
```

Response:
```json
{
  "active_provider": "groq",
  "configured_providers": ["groq", "openai"],
  "available_providers": [
    {
      "name": "groq",
      "display_name": "Groq (Fast & Cheap)",
      "requires_key": true,
      "installed": true
    },
    ...
  ]
}
```

### Set LLM Provider

```bash
POST /api/llm/set-provider
Content-Type: application/json

{
  "provider": "groq",
  "api_key": "gsk_..."  // Optional for Ollama, required for others
}
```

Response:
```json
{
  "message": "LLM provider set to groq",
  "provider": "groq",
  "active_provider": "groq"
}
```

## Environment Configuration (.env)

### Required Variables for Each Provider

**Groq**:
```
GROQ_API_KEY=gsk_...
```

**OpenAI**:
```
OPENAI_API_KEY=sk-...
```

**Anthropic**:
```
ANTHROPIC_API_KEY=sk-ant-...
```

**Google Gemini**:
```
GOOGLE_API_KEY=...
```

**OpenRouter**:
```
OPENROUTER_API_KEY=...
```

**Ollama**:
```
# No API key needed - just ensure Ollama is running
# Optional: specify Ollama server URL
OLLAMA_BASE_URL=http://localhost:11434
```

## Provider Comparison

| Provider | Cost | Speed | Quality | Setup | Best For |
|----------|------|-------|---------|-------|----------|
| **Groq** | 💰💰 | ⚡⚡⚡ | ⭐⭐⭐ | 2min | Production use |
| **Ollama** | Free | ⚡⚡ | ⭐⭐ | 10min | Local privacy |
| **OpenAI** | 💰💰💰 | ⚡⚡ | ⭐⭐⭐⭐ | 1min | Best quality |
| **Claude** | 💰💰💰 | ⚡⚡ | ⭐⭐⭐ | 1min | High quality |
| **Gemini** | 💰💰 | ⚡⚡ | ⭐⭐⭐ | 1min | Google ecosystem |
| **OpenRouter** | Variable | ⚡⚡ | Variable | 1min | Model flexibility |

## Switching Providers at Runtime

### Through Frontend

1. Go to **Settings** → **LLM Provider Configuration**
2. Select a new provider
3. Enter API key (if required)
4. Click **Set Provider**
5. All subsequent searches will use the new provider

### Through API

```bash
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "api_key": "sk-..."
  }'
```

### Through Environment

Edit `.env` file:
```bash
# Deactivate current provider
GROQ_API_KEY=

# Activate new provider
OPENAI_API_KEY=sk-...
```

Then restart the backend:
```bash
# Kill current process and restart
python -m uvicorn backend.app:app --reload
```

## Troubleshooting

### "Provider not installed"
```bash
# Install the required package
pip install [provider-name]
# Examples:
pip install groq
pip install openai
pip install anthropic
pip install google-generativeai
```

### API Key Invalid
- Verify your API key is correct in the Settings page
- Check provider's dashboard/console for active keys
- Ensure API key hasn't been revoked or expired

### No active provider (falling back to Ollama)
- If no provider is configured, system defaults to Ollama
- Install and start Ollama: `ollama serve`
- Or configure another provider in Settings

### Slow responses
- If using Ollama locally, ensure you have adequate system resources
- Consider switching to Groq for faster responses
- Check network connectivity for cloud providers

### Cover letter generation fails
- Ensure the active provider is properly configured
- Try switching to a different provider
- Check backend logs for detailed error messages

## Best Practices

1. **For Development**: Use Ollama (local, free, no API keys)
2. **For Production**: Use Groq (fast, cheap, reliable)
3. **For Best Quality**: Use OpenAI GPT-4
4. **For Cost-Consciousness**: Use Groq or Ollama
5. **For Privacy**: Use Ollama (everything stays local)

## Getting API Keys

### Groq
1. Visit https://console.groq.com
2. Sign up with email or Google account
3. Go to API Keys section
4. Create new API key
5. Copy and save securely

### OpenAI
1. Visit https://platform.openai.com
2. Sign up or login
3. Go to API keys page
4. Create new secret key
5. Copy immediately (you won't see it again)

### Anthropic
1. Visit https://console.anthropic.com
2. Sign up
3. Go to API keys section
4. Create new API key
5. Copy and save securely

### Google Gemini
1. Visit https://makersuite.google.com/app/apikeys
2. Click "Create API key"
3. Select or create a Google Cloud project
4. Copy the generated key

### OpenRouter
1. Visit https://openrouter.ai
2. Sign up
3. Go to dashboard
4. Copy your API key from the left sidebar

## Switching Back to Default

To reset to default (Ollama) configuration:

```bash
# Through frontend
Settings → LLM Provider Configuration → Select "Local Ollama" → Set Provider

# Through API
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "ollama"}'

# Through .env (remove all API keys)
# Delete or comment out OPENAI_API_KEY, GROQ_API_KEY, etc.
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review provider-specific documentation
3. Check backend logs: `tail -f backend.log`
4. Verify network connectivity and API key validity

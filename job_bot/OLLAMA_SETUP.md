# Ollama Setup Guide

Job Bot now uses **Ollama** — a free, local LLM that runs on your machine. No API costs, no rate limits, no data sent to external servers.

## Installation

### macOS
```bash
# Download from https://ollama.ai or use Homebrew
brew install ollama

# Start Ollama
ollama serve
```

### Linux
```bash
# Download from https://ollama.ai or use:
curl https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve
```

### Windows
- Download installer from https://ollama.ai
- Run installer
- Ollama starts automatically in background

## Pulling Models

After Ollama is running, pull a model in a new terminal:

```bash
ollama pull mistral        # Recommended: fast & good quality (4.1GB)
ollama pull neural-chat    # Optimized for chat (4.1GB)
ollama pull orca-mini      # Lightweight (1.3GB) - good for older machines
ollama pull zephyr         # Fast & accurate (2.6GB)
ollama pull llama2         # Meta's Llama (3.8GB)
```

**First time tip**: The first pull takes a few minutes depending on your internet speed. Subsequent pulls are instant.

## Quick Test

```bash
# Test the model directly
ollama run mistral

# Type your prompt, press Enter twice to submit
# Press Ctrl+D to exit
```

## Configuration for Job Bot

In your `.env` file:

```ini
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

If Ollama is on a different machine:
```ini
OLLAMA_BASE_URL=http://192.168.1.100:11434
OLLAMA_MODEL=mistral
```

## Model Recommendations

| Model | Size | Speed | Quality | Use Case |
|---|---|---|---|---|
| **mistral** | 4.1GB | Fast ⚡⚡ | Good 👍 | **Recommended** - best balance |
| orca-mini | 1.3GB | Very Fast ⚡⚡⚡ | OK 👌 | Low-end hardware (< 4GB RAM) |
| neural-chat | 4.1GB | Fast ⚡⚡ | Good 👍 | Optimized for conversations |
| zephyr | 2.6GB | Medium ⚡ | Excellent ⭐ | Best quality if hardware allows |
| llama2 | 3.8GB | Medium ⚡ | Very Good ⭐ | Good alternative to Mistral |

## Troubleshooting

### "Connection refused" error
- Make sure Ollama is running: `ollama serve`
- Check port 11434 is accessible: `curl http://localhost:11434/api/tags`

### Model runs out of memory
- Use a smaller model: `ollama pull orca-mini`
- Or pull and run: `ollama run mistral` first to verify it works

### Slow responses
- Make sure you have GPU acceleration enabled (CUDA on Linux, Metal on macOS)
- Check if other processes are consuming CPU/RAM
- Try a smaller/faster model (orca-mini)

### Model not found after pull
- Verify pull completed: `ollama list`
- Try pulling again: `ollama pull mistral`

## Performance Tips

1. **Use GPU if available** — Ollama auto-detects NVIDIA/AMD GPUs
2. **Keep models on fast storage** — SSD much faster than HDD
3. **Monitor RAM** — Mistral needs ~4-6GB RAM available
4. **Close other apps** — Free up CPU/RAM for faster inference

## Advanced: Custom Models

You can use any GGUF-format model with Ollama:

```bash
# Create Modelfile with custom model
cat > Modelfile << EOF
FROM /path/to/model.gguf
PARAMETER temperature 0.7
PARAMETER top_p 0.9
EOF

# Create custom model
ollama create my-model -f Modelfile

# Use in Job Bot
# Edit .env: OLLAMA_MODEL=my-model
```

## Resources

- **Ollama Docs**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.ai/library
- **Community Models**: https://huggingface.co

## Privacy & Offline

✅ **All processing is local** — your resume and job data never leave your machine  
✅ **Works offline** — once models are downloaded, no internet needed  
✅ **No subscriptions** — completely free  
✅ **No tracking** — Ollama doesn't collect telemetry  

---

Need help? Check Job Bot's README.md or raise an issue on GitHub.

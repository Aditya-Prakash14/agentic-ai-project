# Job Bot API Documentation

Complete REST API documentation for Job Bot backend.

## Base URL

```
http://localhost:8000/api
```

## Health & Config Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

### Get Configuration

```http
GET /config
```

**Response:**
```json
{
  "fit_score_threshold": 65,
  "max_results": 5,
  "enable_apply": false,
  "auto_apply": false
}
```

---

## 🆕 LLM Provider Endpoints

### Get LLM Configuration

Get available LLM providers and active provider configuration.

```http
GET /llm/config
```

**Response:**
```json
{
  "active_provider": "groq",
  "available_providers": [
    {
      "name": "groq",
      "display_name": "Groq (Fast & Cheap)",
      "requires_key": true,
      "installed": true
    },
    {
      "name": "openai",
      "display_name": "OpenAI (GPT-4/3.5)",
      "requires_key": true,
      "installed": true
    },
    {
      "name": "anthropic",
      "display_name": "Anthropic Claude",
      "requires_key": true,
      "installed": false
    },
    {
      "name": "google",
      "display_name": "Google Gemini",
      "requires_key": true,
      "installed": false
    },
    {
      "name": "openrouter",
      "display_name": "OpenRouter",
      "requires_key": true,
      "installed": true
    },
    {
      "name": "ollama",
      "display_name": "Local Ollama",
      "requires_key": false,
      "installed": true
    }
  ],
  "configured_providers": [
    "groq",
    "openai"
  ]
}
```

**Fields:**
- `active_provider` (string) - Currently active LLM provider
- `available_providers` (array) - All available providers with details
- `configured_providers` (array) - Providers that have API keys configured
- `requires_key` (boolean) - Whether provider requires an API key
- `installed` (boolean) - Whether provider package is installed

### Set LLM Provider

Set the active LLM provider. Requires API key for providers that need it.

```http
POST /llm/set-provider
Content-Type: application/json

{
  "provider": "groq",
  "api_key": "gsk_..."
}
```

**Parameters:**
- `provider` (string, required) - Provider name (groq, openai, anthropic, google, openrouter, ollama)
- `api_key` (string, optional) - API key for the provider (required for all except ollama)

**Response:**
```json
{
  "message": "LLM provider set to groq",
  "provider": "groq",
  "active_provider": "groq"
}
```

**Errors:**
- `400 Bad Request` - Unknown provider or provider not installed
- `400 Bad Request` - API key required but not provided
- `400 Bad Request` - Provider not installed (requires pip install)

**Examples:**

Set Groq with API key:
```bash
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "groq",
    "api_key": "gsk_..."
  }'
```

Switch to Ollama (no API key):
```bash
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "ollama"}'
```

Switch to OpenAI:
```bash
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "api_key": "sk-..."
  }'
```

---

## Search Endpoints

### Start Job Search

Start a new job search with query and result limit.

```http
POST /search
Content-Type: application/json

{
  "query": "software engineer internship",
  "num_results": 5
}
```

**Parameters:**
- `query` (string, required) - Search query
- `num_results` (integer, optional, default: 5) - Max results to return

**Response:**
```json
{
  "message": "Search started",
  "query": "software engineer internship",
  "status_url": "/api/search/progress"
}
```

### Get Search Progress

Get real-time progress of ongoing search.

```http
GET /search/progress
```

**Response:**
```json
{
  "is_running": true,
  "progress": 3,
  "total": 5,
  "current_job": "Backend Engineer at Acme Corp",
  "status": "searching"
}
```

**Status Values:**
- `idle` - No search in progress
- `searching` - Search in progress
- `completed` - Search completed successfully
- `error` - Search failed with error

---

## Results Endpoints

### Get All Results

Get paginated list of all job search results.

```http
GET /results
```

**Query Parameters:**
- `skip` (integer, default: 0) - Skip first N results
- `limit` (integer, default: 50) - Limit results to N

**Response:**
```json
{
  "total": 150,
  "results": [
    {
      "id": "abc123def456",
      "title": "Backend Engineer",
      "url": "https://job.example.com/123",
      "snippet": "We're looking for a backend engineer...",
      "fit_score": 87,
      "strengths": ["Python", "REST APIs", "Databases"],
      "gaps": ["DevOps", "Kubernetes"],
      "timestamp": "2024-01-15T10:30:00",
      "cover_letter": "Dear Hiring Manager...",
      "applied": false
    },
    ...
  ]
}
```

### Get Job Detail

Get detailed information for a specific job.

```http
GET /results/{jobId}
```

**Response:**
```json
{
  "id": "abc123def456",
  "title": "Backend Engineer",
  "url": "https://job.example.com/123",
  "snippet": "We're looking for a backend engineer...",
  "fit_score": 87,
  "strengths": ["Python", "REST APIs", "Databases"],
  "gaps": ["DevOps", "Kubernetes"],
  "timestamp": "2024-01-15T10:30:00",
  "cover_letter": "Dear Hiring Manager...",
  "applied": false
}
```

### Get Cover Letter

Get the generated cover letter for a job.

```http
GET /results/{jobId}/cover-letter
```

**Response:**
```json
{
  "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Backend Engineer position..."
}
```

**Errors:**
- `404 Not Found` - Job not found
- `404 Not Found` - No cover letter for job

### Apply to Job

Mark a job as applied.

```http
POST /results/{jobId}/apply
```

**Response:**
```json
{
  "message": "Job marked as applied",
  "id": "abc123def456"
}
```

### Delete Result

Delete a job from results.

```http
DELETE /results/{jobId}
```

**Response:**
```json
{
  "message": "Result deleted",
  "id": "abc123def456"
}
```

---

## Statistics Endpoints

### Get Statistics

Get overall statistics about job search results.

```http
GET /stats
```

**Response:**
```json
{
  "total_jobs": 150,
  "high_fit_jobs": 42,
  "applied": 8,
  "pending": 34,
  "average_fit_score": 68.5
}
```

**Fields:**
- `total_jobs` - Total jobs analyzed
- `high_fit_jobs` - Jobs with fit_score ≥ threshold
- `applied` - Jobs marked as applied
- `pending` - High-fit jobs not yet applied to
- `average_fit_score` - Average fit score across all jobs

---

## Tracker Endpoints

### Reset Tracker

Reset the job tracker (delete all results).

```http
POST /reset
```

**Response:**
```json
{
  "message": "Tracker reset"
}
```

**⚠️ WARNING**: This action is irreversible and will delete all stored results!

---

## Error Handling

### Error Response Format

All errors return a JSON response with HTTP status codes:

```json
{
  "detail": "Error message here"
}
```

### Common Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `409 Conflict` - Search already in progress
- `500 Internal Server Error` - Server error

### Common Errors

**Provider Not Installed:**
```json
{
  "detail": "Provider 'groq' is not installed. Run: pip install groq"
}
```

**API Key Required:**
```json
{
  "detail": "Provider 'openai' requires an API key"
}
```

**Search Already Running:**
```json
{
  "detail": "Search already in progress"
}
```

---

## Complete Example Workflow

### 1. Check Available Providers

```bash
curl http://localhost:8000/api/llm/config
```

### 2. Set LLM Provider

```bash
curl -X POST http://localhost:8000/api/llm/set-provider \
  -H "Content-Type: application/json" \
  -d '{"provider": "groq", "api_key": "gsk_..."}'
```

### 3. Start Search

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "software engineer internship",
    "num_results": 5
  }'
```

### 4. Monitor Progress

```bash
curl http://localhost:8000/api/search/progress
```

### 5. Get Results

```bash
curl http://localhost:8000/api/results
```

### 6. Get Statistics

```bash
curl http://localhost:8000/api/stats
```

### 7. Apply to Job

```bash
curl -X POST http://localhost:8000/api/results/abc123/apply
```

---

## Rate Limiting

- No explicit rate limits (modify as needed for production)
- 1-second delay between search API calls (configurable)
- Respect third-party API rate limits

---

## Authentication

Currently no authentication required. For production, implement:

- API key authentication
- JWT tokens
- OAuth 2.0
- Rate limiting per user

---

## CORS

Frontend is configured to access API at:
- http://localhost:5173 (development)
- http://localhost:3000 (alternative)

---

## Swagger Documentation

Interactive API documentation available at:

```
http://localhost:8000/docs
```

This provides a visual interface to test all endpoints!

---

## SDK/Client Libraries

### Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Get LLM config
response = requests.get(f"{BASE_URL}/llm/config")
config = response.json()

# Set provider
response = requests.post(
  f"{BASE_URL}/llm/set-provider",
  json={"provider": "groq", "api_key": "gsk_..."}
)

# Start search
response = requests.post(
  f"{BASE_URL}/search",
  json={"query": "software engineer", "num_results": 5}
)
```

### JavaScript/TypeScript

```javascript
const BASE_URL = "http://localhost:8000/api";

// Get LLM config
const config = await fetch(`${BASE_URL}/llm/config`).then(r => r.json());

// Set provider
const result = await fetch(`${BASE_URL}/llm/set-provider`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ provider: "groq", api_key: "gsk_..." })
}).then(r => r.json());

// Start search
const search = await fetch(`${BASE_URL}/search`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ query: "software engineer", num_results: 5 })
}).then(r => r.json());
```

---

## Deployment

### Environment Variables

```bash
# Backend
GROQ_API_KEY=gsk_...
OPENAI_API_KEY=sk-...
FIT_SCORE_THRESHOLD=65
MAX_RESULTS_PER_QUERY=5
```

### Docker

```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Support

For issues or questions:
1. Check [LLM_PROVIDERS.md](../LLM_PROVIDERS.md)
2. Visit http://localhost:8000/docs for interactive testing
3. Check backend logs for error details
4. Review [README.md](../README.md)

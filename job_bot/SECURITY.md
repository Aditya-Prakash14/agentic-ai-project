# Security Best Practices

Protecting your API keys, resume, and personal data.

---

## 🔑 API Keys & Secrets

### DO ✅

- ✅ Store API keys in `.env` file (never in code)
- ✅ Use `.env.example` to document required variables
- ✅ Add `.env` to `.gitignore` (prevents accidental commits)
- ✅ Rotate API keys periodically
- ✅ Use separate API keys for different environments (dev, prod)
- ✅ Review `.env` file permissions: `chmod 600 .env`

### DON'T ❌

- ❌ Commit `.env` to version control
- ❌ Share API keys in public repos, Slack, or email
- ❌ Hard-code secrets in Python files
- ❌ Log or print API keys in terminal/logs
- ❌ Use the same API key across multiple machines/projects

### If You Accidentally Expose a Key

1. **Immediately revoke it** on the service (e.g., serper.dev dashboard)
2. **Generate a new key** and update `.env`
3. **Force-push to git** if committed (⚠️ only if repo is private):
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   git push -f origin main
   ```
4. **Notify team members** if shared repository

---

## 📄 Resume & Personal Data

### DO ✅

- ✅ Keep `resume.txt` in `.gitignore` if it contains personal info
- ✅ Use generic versions for public sharing
- ✅ Review generated cover letters before applying
- ✅ Store sensitive files locally only

### DON'T ❌

- ❌ Commit your resume to version control
- ❌ Share your resume in public repos
- ❌ Leave contact info in code/comments

---

## 🔐 Environment Security

### Local Development

```bash
# Secure .env file permissions (Linux/macOS)
chmod 600 .env

# Verify permissions
ls -la .env
# Should show: -rw------- (only owner can read/write)
```

### GitHub Best Practices

```bash
# Verify .env is in .gitignore
cat .gitignore | grep "^\.env$"

# Check nothing sensitive is staged
git diff --cached | grep -i "api_key\|password\|token"

# Safe to commit?
git status
```

---

## 🛡️ API Key Rotation

### Serper API

1. Go to [serper.dev/dashboard](https://serper.dev/dashboard)
2. Click "API Key" section
3. Generate a new key
4. Update `.env` with new key:
   ```bash
   echo "SERPER_API_KEY=your_new_key" >> .env
   ```
5. Delete old key in dashboard

### Schedule Rotation

- **Recommended:** Every 90 days
- **Or:** If key is ever exposed
- **Or:** If team member leaves

---

## 🚨 Threat Model

### What Could Go Wrong?

| Threat | Impact | Mitigation |
|--------|--------|------------|
| API key exposed on GitHub | Attacker can make API calls on your dime | Use `.gitignore`, scan commits with `git-secrets` |
| Resume leaked | Identity theft, targeted phishing | Keep out of git, local-only storage |
| Ollama credentials stored | Unauthorized ML inference | Ollama has no auth by default (only expose on localhost) |
| Playwright sessions logged | Session hijacking | Don't log sensitive browser data |

---

## 🔍 Security Scanning

### Pre-Commit Hook (Prevent accidental secrets commit)

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
if git diff --cached | grep -E "SERPER_API_KEY|password|token" > /dev/null; then
  echo "❌ Error: Secrets detected in staged files!"
  exit 1
fi
```

### Manual Scan

```bash
# Check for common secrets patterns
git diff --cached | grep -i "api.key\|password\|secret\|token"

# Scan entire repo history
git log -p | grep -i "SERPER_API_KEY"
```

---

## 📋 Checklist Before Sharing

Before pushing to GitHub (even private):

- [ ] `.env` is in `.gitignore`
- [ ] No API keys in Python files
- [ ] No API keys in git history: `git log | grep -i "api_key"`
- [ ] `resume.txt` is in `.gitignore` (if personal)
- [ ] `.env` file is not tracked: `git ls-files | grep .env`
- [ ] Permissions on `.env`: `chmod 600 .env`

---

## 🔄 Incident Response

If you suspect a breach:

1. **Check logs** — Review Serper dashboard for unusual activity
2. **Revoke keys** — Immediately rotate all API keys
3. **Audit code** — Search git history for leaks
4. **Notify team** — If shared repository
5. **Update secrets** — Generate new `.env` with fresh keys

---

## 📚 Additional Resources

- [OWASP: Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Git Secrets Tool](https://github.com/awslabs/git-secrets)
- [Serper API Security](https://serper.dev/docs)
- [Python-Dotenv Docs](https://python-dotenv.readthedocs.io)

---

**Remember:** The best security is prevention. Treat `.env` like a password — never share it, never commit it, never log it. ✅

# 🛡️ Security Policy

> "The best defense is a good offense... but in security, the best offense is a good defense!" — Security-conscious Trainer

## Supported Versions 📊

We actively support security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

---

## Reporting a Vulnerability 🔐

We take security seriously at PokéRAG! If you discover a security vulnerability, please report it responsibly.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please:

1. **Email us** at: `security@your-domain.com` (or use GitHub's private vulnerability reporting)
2. **Include** the following information:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes

### What to Expect

| Timeline | Action |
|----------|--------|
| **24 hours** | We'll acknowledge receipt of your report |
| **72 hours** | We'll provide an initial assessment |
| **7 days** | We'll have a plan for addressing the issue |
| **30 days** | We aim to have a fix released (severity dependent) |

### Our Commitment

- We will not take legal action against you for responsibly disclosing security issues
- We will work with you to understand and resolve the issue quickly
- We will credit you in our security acknowledgments (unless you prefer anonymity)

---

## Security Best Practices 🔒

### For Users

#### API Keys
```bash
# ❌ DON'T: Commit API keys to version control
OPENAI_API_KEY=sk-actual-key-here

# ✅ DO: Use .env files (never committed)
# Add to .gitignore:
.env
.env.local
*.env
```

#### Environment Files
- Never commit `.env` files to version control
- Use `.env.example` as a template (without real values)
- Rotate keys if accidentally exposed

#### Network Security
- Use HTTPS in production
- Configure CORS appropriately
- Don't expose internal endpoints publicly

### For Developers

#### Dependencies
```bash
# Regularly update dependencies
pip install --upgrade -r requirements.txt
pnpm update

# Check for known vulnerabilities
pip-audit  # For Python
pnpm audit  # For Node.js
```

#### Input Validation
- Never trust user input
- Sanitize file uploads
- Validate query parameters

#### Secrets Management
- Use environment variables for secrets
- Consider using a secrets manager for production
- Rotate credentials regularly

---

## Known Security Considerations ⚠️

### API Endpoints

| Endpoint | Consideration |
|----------|---------------|
| `/chat` | Rate limiting recommended for production |
| `/add/*` | File upload validation in place |
| `/ingest` | Should be protected in production |
| `/process` | Should be protected in production |

### File Uploads

The file upload feature (`/add/text`, `/add/image`, `/add/audio`) includes:
- File type validation
- Size limits (recommended to configure)
- Secure file storage

**Recommendation**: In production, add:
- Virus/malware scanning
- Stricter file type validation
- File size limits

### Vector Database (Qdrant)

- Uses API key authentication
- Ensure your Qdrant cluster is not publicly accessible
- Use network isolation in production

### LLM Interactions (OpenAI)

- API key required for all requests
- Be aware of prompt injection risks
- Monitor usage and costs

---

## Security Checklist for Production 📋

Before deploying to production, ensure:

### Infrastructure
- [ ] HTTPS enabled with valid certificates
- [ ] API keys stored securely (not in code)
- [ ] Firewall configured appropriately
- [ ] Database access restricted
- [ ] Logging enabled for security events

### Application
- [ ] CORS configured for specific origins only
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Admin endpoints protected

### Monitoring
- [ ] Security logging enabled
- [ ] Alerts for suspicious activity
- [ ] Regular dependency audits scheduled
- [ ] Backup strategy in place

---

## Security Features 🛡️

### Built-in Protections

| Feature | Description |
|---------|-------------|
| **CORS** | Configured in `api/main.py` |
| **Input Validation** | Pydantic models for request validation |
| **Dependency Isolation** | Virtual environment recommended |
| **No Hardcoded Secrets** | All secrets via environment variables |

### Recommended Additions for Production

```python
# Example: Add rate limiting with slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")
async def chat(request: Request, message: str):
    ...
```

---

## Acknowledgments 🙏

We thank the following security researchers for responsibly disclosing vulnerabilities:

*No vulnerabilities reported yet — be the first responsible reporter!*

---

## Contact 📧

For security concerns:
- **Email**: security@your-domain.com
- **GitHub**: Use private vulnerability reporting

For general questions:
- Open a GitHub Discussion
- Check our documentation

---

<p align="center">
  <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/208.png" width="80" alt="Steelix">
</p>

<p align="center">
  <em>"Be as strong as Steelix when protecting user data!"</em>
</p>

<p align="center">
  <strong>Security is everyone's responsibility 🔐</strong>
</p>

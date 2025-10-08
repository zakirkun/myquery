# Security Policy

## 🔒 Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## 🐛 Reporting a Vulnerability

If you discover a security vulnerability in MyQuery, please **DO NOT** create a public GitHub issue.

### How to Report

1. **Email** the security issue to: **zakir@gnuweeb.org**
2. **Include** the following information:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **24 hours**: Initial response
- **72 hours**: Assessment and confirmation
- **7 days**: Fix and disclosure plan
- **30 days**: Public disclosure (after fix is released)

## 🛡️ Security Measures

### Dependency Scanning

We use:
- **Dependabot** untuk automatic dependency updates
- **Trivy** untuk vulnerability scanning
- **CodeQL** untuk code analysis

### Best Practices

MyQuery follows security best practices:

1. **Input Validation**
   - Semua user input di-validate
   - SQL injection prevention via parameterized queries
   - XSS prevention di Web UI

2. **Authentication & Authorization**
   - API key encryption
   - Secure credential storage
   - No hardcoded secrets

3. **Data Protection**
   - Encrypted connections (TLS/SSL)
   - No logging of sensitive data
   - Secure environment variable handling

4. **Dependencies**
   - Regular updates
   - Security patches prioritized
   - Minimal dependencies

## 🔐 Security Features

### Database Connections

```python
# Secure connection dengan SSL
myquery connect --db-type postgresql \
  --db-ssl-mode require \
  --db-ssl-cert /path/to/cert.pem
```

### Environment Variables

```bash
# Store credentials securely
export OPENAI_API_KEY="sk-..."
export DB_PASSWORD="..."

# Never commit .env files
echo ".env" >> .gitignore
```

### API Key Management

```python
# Keys stored in encrypted format
# Never logged or exposed in errors
```

## 📋 Security Checklist for Contributors

Before submitting code:

- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] Dependencies up to date
- [ ] No security warnings in linters
- [ ] Secrets properly handled
- [ ] SQL queries parameterized
- [ ] Error messages don't expose sensitive info

## 🚨 Known Security Considerations

### OpenAI API

- API keys must be kept confidential
- Rate limiting implemented
- Data is not stored on OpenAI servers (except their logging)

### Database Credentials

- Use .env files or environment variables
- Never commit credentials to git
- Use connection pooling with authentication timeout

### Web UI

- CORS properly configured
- XSS prevention implemented
- CSRF tokens for forms

## 🔄 Security Updates

Subscribe untuk security updates:

- **GitHub Watch** → Custom → Security alerts
- **Email**: Subscribe di repository
- **RSS**: https://github.com/zakirkun/myquery/releases.atom

## 📚 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

## 🙏 Recognition

We appreciate responsible disclosure. Security researchers who report valid vulnerabilities will:

- Be credited in SECURITY.md (optional)
- Receive credit in release notes
- Receive swag/merchandise (for critical vulnerabilities)

## 📞 Contact

- **Security Email**: zakir@gnuweeb.org
- **General Issues**: https://github.com/zakirkun/myquery/issues
- **Private**: Contact maintainers directly via GitHub

---

Thank you for helping keep MyQuery secure! 🙏


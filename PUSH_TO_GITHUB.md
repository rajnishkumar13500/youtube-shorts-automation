# Push to GitHub Checklist

Follow this checklist before pushing your code to GitHub.

---

## ⚠️ CRITICAL: Remove Sensitive Files

Before pushing, ensure these files are NOT in your repository:

### Check for Sensitive Files

```bash
# Check what will be committed
git status

# Look for these files (MUST NOT be present):
# ❌ .env
# ❌ *.json (credentials)
# ❌ youtube_token.pickle
# ❌ Any API keys or secrets
```

### Remove Sensitive Files (if present)

```bash
# Remove from git tracking
git rm --cached .env
git rm --cached *.json
git rm --cached youtube_token.pickle

# Verify .gitignore
cat .gitignore
```

---

## Pre-Push Checklist

- [ ] **Remove .env file** (contains API keys)
- [ ] **Remove all .json credential files**
- [ ] **Remove youtube_token.pickle**
- [ ] **Verify .gitignore is working**
- [ ] **Keep .env.example** (template only, no real keys)
- [ ] **Keep all .py files**
- [ ] **Keep all .md documentation**
- [ ] **Keep .github/workflows/ directory**

---

## Step-by-Step Push Instructions

### 1. Initialize Git (if not already done)

```bash
git init
```

### 2. Verify .gitignore

```bash
# Check .gitignore exists and has correct content
cat .gitignore

# Should include:
# .env
# *.json
# youtube_token.pickle
```

### 3. Check Status

```bash
git status

# Verify NO sensitive files are listed
# If you see .env or .json files, STOP and remove them
```

### 4. Add Files

```bash
# Add all files (sensitive files will be ignored by .gitignore)
git add .

# Verify what will be committed
git status
```

### 5. Commit

```bash
git commit -m "Initial commit - YouTube Shorts Automation"
```

### 6. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `youtube-shorts-automation`
3. Visibility: **Public** (for free GitHub Actions)
4. Don't initialize with README
5. Click "Create repository"

### 7. Add Remote and Push

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/youtube-shorts-automation.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## After Pushing

### 1. Verify Repository

Go to your repository on GitHub and verify:
- [ ] No .env file visible
- [ ] No .json credential files visible
- [ ] No youtube_token.pickle visible
- [ ] All .py files are present
- [ ] All .md files are present
- [ ] .github/workflows/ directory is present

### 2. Add GitHub Secrets

Go to: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets:

| Secret Name | Value Source |
|------------|--------------|
| `GROQ_API_KEY` | From your local .env file |
| `ELEVENLABS_API_KEY` | From your local .env file |
| `ELEVENLABS_API_KEY_2` | From your local .env file (optional) |
| `ELEVENLABS_API_KEY_3` | From your local .env file (optional) |
| `CLOUDFLARE_ACCOUNT_ID` | From your local .env file |
| `CLOUDFLARE_API_TOKEN` | From your local .env file |
| `GOOGLE_SHEETS_ID` | From your local .env file |
| `GOOGLE_SHEETS_CREDENTIALS` | Full JSON content from credentials file |
| `YOUTUBE_CLIENT_SECRETS` | Full JSON content from client secrets file |
| `YOUTUBE_TOKEN` | Base64 encoded youtube_token.pickle |

### 3. Encode YouTube Token

```bash
# On Windows (PowerShell)
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) > youtube_token_base64.txt

# On Linux/Mac
base64 youtube_token.pickle > youtube_token_base64.txt

# Copy content and add as YOUTUBE_TOKEN secret
cat youtube_token_base64.txt
```

### 4. Enable GitHub Actions

1. Go to **Actions** tab
2. Click "I understand my workflows, go ahead and enable them"

### 5. Test Setup

1. Go to **Actions** tab
2. Click **Test Setup** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for completion
5. Verify green checkmark ✓

---

## Quick Commands

```bash
# Full push sequence
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/youtube-shorts-automation.git
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "Remote already exists"

```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/youtube-shorts-automation.git
```

### "Permission denied"

```bash
# Use HTTPS with token or SSH key
# Or authenticate with GitHub CLI
gh auth login
```

### Accidentally Committed Sensitive Files

```bash
# Remove from git history
git rm --cached .env
git rm --cached *.json
git commit -m "Remove sensitive files"
git push --force
```

**⚠️ Important:** If you accidentally pushed API keys:
1. Immediately revoke/regenerate all API keys
2. Update secrets in GitHub
3. Remove files from git history

---

## Next Steps

After successful push:

1. ✅ **Read:** `GITHUB_ACTIONS_SETUP.md`
2. ✅ **Add all secrets** in GitHub Settings
3. ✅ **Test workflow** from Actions tab
4. ✅ **Generate first video** manually
5. ✅ **Enable scheduled automation**

---

## Security Reminders

- ✅ Never commit .env file
- ✅ Never commit .json credential files
- ✅ Never commit API keys or tokens
- ✅ Always use GitHub Secrets for sensitive data
- ✅ Make repository private if handling sensitive content
- ✅ Rotate API keys regularly
- ✅ Review commits before pushing

---

**Ready to push?** Follow the checklist above carefully!

After pushing, continue with: `GITHUB_ACTIONS_SETUP.md`

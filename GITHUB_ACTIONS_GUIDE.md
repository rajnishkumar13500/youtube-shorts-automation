# GitHub Actions Deployment Guide

Use GitHub Actions to run your YouTube Shorts automation for FREE! No cloud server needed.

---

## ⚠️ Important Limitations

Before using GitHub Actions, understand these constraints:

### Pros ✅
- **100% FREE** (2,000 minutes/month on free plan)
- No server management
- Easy setup
- Automatic scheduling
- Built-in logging

### Cons ❌
- **6-hour workflow limit** (videos must complete in 6 hours)
- **Scheduled workflows run every 5 minutes minimum** (not exact times)
- **Delays of 3-10 minutes** are common during high load
- **Public repos only** for free (private repos use paid minutes)
- **No persistent storage** (files deleted after workflow)
- **YouTube token expires** (need to re-authenticate periodically)

### Verdict
✅ **Good for:** Testing, low-volume posting (1-3 videos/day)  
❌ **Not ideal for:** High-volume, precise timing, long-term automation

---

## Setup Guide

### Step 1: Create GitHub Repository

1. Create a new repository on GitHub
2. Make it **public** (to use free Actions minutes)
3. Clone to your local machine

```bash
git clone https://github.com/yourusername/youtube-automation.git
cd youtube-automation
```

### Step 2: Add Secrets

Go to your repository on GitHub:
1. Click **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**
3. Add these secrets:

| Secret Name | Value |
|------------|-------|
| `GROQ_API_KEY` | Your Groq API key |
| `ELEVENLABS_API_KEY` | Your ElevenLabs API key |
| `ELEVENLABS_API_KEY_2` | Fallback token (optional) |
| `ELEVENLABS_API_KEY_3` | Fallback token (optional) |
| `CLOUDFLARE_ACCOUNT_ID` | Your Cloudflare account ID |
| `CLOUDFLARE_API_TOKEN` | Your Cloudflare API token |
| `GOOGLE_SHEETS_CREDENTIALS` | Full JSON content of credentials file |
| `GOOGLE_SHEETS_ID` | Your spreadsheet ID |
| `YOUTUBE_CLIENT_SECRETS` | Full JSON content of client secrets |
| `YOUTUBE_TOKEN` | Base64 encoded youtube_token.pickle |

### Step 3: Encode YouTube Token

The YouTube token needs special encoding:

```bash
# On your local machine (after authenticating YouTube)
base64 youtube_token.pickle > youtube_token_base64.txt

# Copy the content and add as YOUTUBE_TOKEN secret
cat youtube_token_base64.txt
```

### Step 4: Create Workflow Files

I'll create the workflow files for you in the next step.

---

## Workflow Options

### Option A: 3 Videos Daily (Recommended)

Posts 3 videos per day at approximately:
- 9:00 AM
- 3:00 PM
- 9:00 PM

**Note:** GitHub Actions may delay by 3-10 minutes.

### Option B: Single Video on Demand

Manually trigger video generation from GitHub Actions tab.

### Option C: Continuous (Every 8 Hours)

Posts 1 video every 8 hours automatically.

---

## Cost Comparison

### GitHub Actions (Free Tier)

| Plan | Minutes/Month | Cost | Videos/Month |
|------|---------------|------|--------------|
| Free | 2,000 | $0 | ~400 videos |
| Pro | 3,000 | $4 | ~600 videos |
| Team | 10,000 | $21 | ~2,000 videos |

**Calculation:** Each video takes ~5 minutes = 2,000 minutes ÷ 5 = 400 videos/month

### Cloud Server

| Platform | Cost/Month | Videos/Month |
|----------|-----------|--------------|
| DigitalOcean | $12 | Unlimited |
| AWS EC2 | $15-30 | Unlimited |
| Google Cloud | $20-35 | Unlimited |

---

## Limitations & Workarounds

### 1. Scheduling Delays

**Problem:** GitHub Actions scheduled workflows can be delayed by 3-10 minutes during high load.

**Workaround:**
- Schedule 5-10 minutes earlier
- Use multiple workflows for redundancy
- Accept approximate timing

### 2. YouTube Token Expiration

**Problem:** YouTube OAuth tokens expire after 7 days of inactivity.

**Workaround:**
- Re-authenticate weekly
- Use refresh token (requires custom implementation)
- Monitor for auth failures

### 3. No Persistent Storage

**Problem:** Files are deleted after each workflow run.

**Workaround:**
- Upload videos to GitHub Releases (not recommended)
- Upload directly to YouTube (current approach)
- Use external storage (S3, Google Drive)

### 4. 6-Hour Timeout

**Problem:** Workflows must complete within 6 hours.

**Workaround:**
- Process one video per workflow
- Optimize video generation speed
- Split into multiple workflows

### 5. Rate Limits

**Problem:** YouTube API has daily quotas.

**Workaround:**
- Limit to 3-5 videos per day
- Monitor quota usage
- Use multiple YouTube accounts (not recommended)

---

## Monitoring & Debugging

### View Workflow Runs

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Click on a workflow run to see logs

### Check Logs

Logs are automatically saved in GitHub Actions:
- Click on workflow run
- Click on job name
- Expand steps to see detailed logs

### Download Artifacts

If you configure artifact upload:
```yaml
- name: Upload logs
  uses: actions/upload-artifact@v3
  with:
    name: logs
    path: output/logs/
```

---

## Security Best Practices

### 1. Use Secrets for All Credentials

Never commit:
- API keys
- Credentials JSON files
- OAuth tokens
- `.env` file

### 2. Use Private Repository

For sensitive projects:
- Make repository private
- Accept paid Actions minutes
- Better security

### 3. Limit Permissions

In workflow file:
```yaml
permissions:
  contents: read
```

### 4. Rotate Secrets Regularly

- Change API keys monthly
- Update YouTube tokens weekly
- Monitor for unauthorized access

---

## Troubleshooting

### Workflow Not Running

**Check:**
1. Repository is public (for free tier)
2. Actions are enabled (Settings > Actions)
3. Cron syntax is correct
4. Secrets are added correctly

### Authentication Failures

**YouTube:**
```bash
# Re-encode token
base64 youtube_token.pickle > youtube_token_base64.txt
# Update YOUTUBE_TOKEN secret
```

**Google Sheets:**
```bash
# Verify JSON format
cat credentials.json | jq .
# Update GOOGLE_SHEETS_CREDENTIALS secret
```

### Video Generation Fails

**Check logs:**
1. Go to Actions tab
2. Click failed workflow
3. Check error messages
4. Verify all secrets are set

### Out of Minutes

**Solutions:**
1. Upgrade to Pro plan ($4/month)
2. Optimize workflow (reduce video count)
3. Switch to cloud server
4. Use multiple GitHub accounts (not recommended)

---

## Migration to Cloud Server

If GitHub Actions doesn't meet your needs:

### When to Migrate

- Need precise scheduling
- High volume (>10 videos/day)
- Long-term automation
- Consistent performance

### Migration Steps

1. Follow `HOSTING_GUIDE.md`
2. Choose cloud platform
3. Deploy using `deploy.sh`
4. Disable GitHub Actions workflows

---

## Hybrid Approach

Use both GitHub Actions and cloud server:

### GitHub Actions
- Testing new features
- Backup automation
- Manual video generation

### Cloud Server
- Primary automation
- Scheduled posting
- High-volume processing

---

## Cost Analysis

### Scenario 1: 3 Videos/Day (90/month)

| Solution | Cost | Pros | Cons |
|----------|------|------|------|
| GitHub Actions | $0 | Free, easy | Delays, limits |
| DigitalOcean | $12 | Reliable, fast | Requires setup |
| AWS EC2 | $15 | Scalable | More complex |

**Recommendation:** Start with GitHub Actions, migrate to cloud if needed.

### Scenario 2: 10 Videos/Day (300/month)

| Solution | Cost | Pros | Cons |
|----------|------|------|------|
| GitHub Actions | $0-4 | Cheap | May hit limits |
| DigitalOcean | $12-24 | Unlimited | Monthly cost |
| AWS EC2 | $30 | Powerful | Higher cost |

**Recommendation:** Use cloud server for reliability.

---

## Quick Start Commands

### Setup Repository

```bash
# Create repository
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/youtube-automation.git
git push -u origin main
```

### Add Secrets via CLI (Optional)

```bash
# Install GitHub CLI
# https://cli.github.com/

# Login
gh auth login

# Add secrets
gh secret set GROQ_API_KEY < groq_key.txt
gh secret set ELEVENLABS_API_KEY < elevenlabs_key.txt
gh secret set GOOGLE_SHEETS_CREDENTIALS < credentials.json
gh secret set YOUTUBE_CLIENT_SECRETS < client_secrets.json

# Encode and add YouTube token
base64 youtube_token.pickle | gh secret set YOUTUBE_TOKEN
```

### Test Workflow

```bash
# Trigger manual workflow
gh workflow run "Generate Video"

# View workflow runs
gh run list

# View logs
gh run view
```

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Add all secrets
3. ✅ Push code to repository
4. ✅ Enable GitHub Actions
5. ✅ Test manual workflow
6. ✅ Enable scheduled workflows
7. ✅ Monitor first few runs

---

## Conclusion

### Use GitHub Actions If:
- Starting out / testing
- Low volume (1-5 videos/day)
- Budget is $0
- Don't need precise timing

### Use Cloud Server If:
- High volume (10+ videos/day)
- Need precise scheduling
- Long-term automation
- Professional use

### Hybrid Approach:
- Use both for redundancy
- GitHub Actions as backup
- Cloud server as primary

---

**Ready to deploy?** I'll create the workflow files next!

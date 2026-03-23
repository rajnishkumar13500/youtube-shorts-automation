# GitHub Actions Setup - Step by Step

Complete guide to deploy your YouTube Shorts automation using GitHub Actions (100% FREE).

---

## Quick Overview

✅ **Cost:** $0 (2,000 free minutes/month)  
✅ **Setup Time:** 15 minutes  
✅ **Maintenance:** Low  
⚠️ **Limitation:** Scheduling delays (3-10 minutes)

---

## Step-by-Step Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `youtube-shorts-automation`
3. **Visibility:** Public (for free Actions minutes)
4. **Initialize:** Don't add README, .gitignore, or license
5. **Click:** Create repository

### Step 2: Push Your Code

From your local project directory:

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - YouTube Shorts Automation"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/youtube-shorts-automation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Add Repository Secrets

Go to your repository on GitHub:

**Settings** → **Secrets and variables** → **Actions** → **New repository secret**

Add these secrets one by one:

#### Required Secrets

| Secret Name | How to Get Value |
|------------|------------------|
| `GROQ_API_KEY` | Copy from your `.env` file |
| `ELEVENLABS_API_KEY` | Copy from your `.env` file |
| `CLOUDFLARE_ACCOUNT_ID` | Copy from your `.env` file |
| `CLOUDFLARE_API_TOKEN` | Copy from your `.env` file |
| `GOOGLE_SHEETS_ID` | Copy from your `.env` file |

#### Optional Secrets (for fallback)

| Secret Name | How to Get Value |
|------------|------------------|
| `ELEVENLABS_API_KEY_2` | Copy from your `.env` file (if you have it) |
| `ELEVENLABS_API_KEY_3` | Copy from your `.env` file (if you have it) |

#### JSON Credentials

**GOOGLE_SHEETS_CREDENTIALS:**
```bash
# Copy entire JSON file content
cat youtube-automation-*.json
# Paste the entire JSON content as secret value
```

**YOUTUBE_CLIENT_SECRETS:**
```bash
# Copy entire JSON file content
cat client_secret_*.json
# Paste the entire JSON content as secret value
```

#### YouTube Token (Important!)

**YOUTUBE_TOKEN:**
```bash
# First, authenticate YouTube locally
python setup_youtube_account.py

# Then encode the token
base64 youtube_token.pickle > youtube_token_base64.txt

# On Windows (PowerShell):
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) > youtube_token_base64.txt

# Copy content and paste as secret
cat youtube_token_base64.txt
```

### Step 4: Enable GitHub Actions

1. Go to your repository
2. Click **Actions** tab
3. Click **I understand my workflows, go ahead and enable them**

### Step 5: Test Setup

1. Go to **Actions** tab
2. Click **Test Setup** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for completion (2-3 minutes)
5. Check for green checkmark ✓

If test passes, you're ready!

### Step 6: Test Video Generation

1. Go to **Actions** tab
2. Click **Generate Single Video (Manual)** workflow
3. Click **Run workflow**
4. Enter:
   - **Topic:** `drinking water benefits`
   - **Duration:** `20`
   - **Upload to YouTube:** `true`
5. Click **Run workflow**
6. Wait 5-10 minutes
7. Check your YouTube channel!

### Step 7: Enable Scheduled Automation

The scheduled workflow is already configured! It will run automatically at:
- 9:00 AM UTC
- 3:00 PM UTC
- 9:00 PM UTC

**Adjust for your timezone:**

Edit `.github/workflows/daily-videos.yml`:

```yaml
schedule:
  # For India (IST = UTC+5:30), subtract 5:30 from desired time
  # 9:00 AM IST = 3:30 AM UTC
  - cron: '30 3 * * *'
  # 3:00 PM IST = 9:30 AM UTC
  - cron: '30 9 * * *'
  # 9:00 PM IST = 3:30 PM UTC
  - cron: '30 15 * * *'
```

Commit and push changes:

```bash
git add .github/workflows/daily-videos.yml
git commit -m "Adjust schedule for timezone"
git push
```

---

## Timezone Conversion

### Common Timezones

| Timezone | UTC Offset | 9 AM Local | 3 PM Local | 9 PM Local |
|----------|-----------|-----------|-----------|-----------|
| IST (India) | +5:30 | 3:30 UTC | 9:30 UTC | 15:30 UTC |
| EST (US East) | -5:00 | 14:00 UTC | 20:00 UTC | 2:00 UTC (next day) |
| PST (US West) | -8:00 | 17:00 UTC | 23:00 UTC | 5:00 UTC (next day) |
| GMT (UK) | +0:00 | 9:00 UTC | 15:00 UTC | 21:00 UTC |
| AEST (Australia) | +10:00 | 23:00 UTC (prev day) | 5:00 UTC | 11:00 UTC |

### Cron Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

Examples:
- `0 9 * * *` = Every day at 9:00 AM UTC
- `30 15 * * *` = Every day at 3:30 PM UTC
- `0 */8 * * *` = Every 8 hours
- `0 9 * * 1-5` = Every weekday at 9:00 AM UTC

---

## Monitoring & Logs

### View Workflow Runs

1. Go to **Actions** tab
2. See all workflow runs
3. Green ✓ = Success
4. Red ✗ = Failed

### View Detailed Logs

1. Click on a workflow run
2. Click on job name (e.g., "generate-and-upload")
3. Expand steps to see logs
4. Download logs if needed

### Download Artifacts

After each run, logs are saved as artifacts:

1. Go to workflow run
2. Scroll to bottom
3. Click **logs-XXX** to download
4. Extract and view logs

### Check YouTube Token

If authentication fails:

1. Go to failed workflow run
2. Download **youtube-token-XXX** artifact
3. Update `YOUTUBE_TOKEN` secret with new value

---

## Troubleshooting

### Workflow Not Running

**Problem:** Scheduled workflow doesn't run

**Solutions:**
1. Check repository is public
2. Verify Actions are enabled
3. Check cron syntax
4. Wait (delays are normal)
5. Trigger manually to test

### Authentication Failed

**Problem:** YouTube or Google Sheets auth fails

**Solutions:**

**YouTube:**
```bash
# Re-authenticate locally
python setup_youtube_account.py

# Re-encode token
base64 youtube_token.pickle > youtube_token_base64.txt

# Update YOUTUBE_TOKEN secret
```

**Google Sheets:**
```bash
# Verify JSON is valid
cat credentials.json | python -m json.tool

# Update GOOGLE_SHEETS_CREDENTIALS secret
```

### Video Generation Failed

**Problem:** Video generation fails

**Check:**
1. View workflow logs
2. Check API keys are correct
3. Verify all secrets are set
4. Test locally first

**Common errors:**
- `GROQ_API_KEY invalid` → Update secret
- `ElevenLabs quota exceeded` → Add fallback keys
- `FFmpeg error` → Check video generation code

### Out of Minutes

**Problem:** Exceeded 2,000 free minutes

**Solutions:**
1. Upgrade to Pro ($4/month for 3,000 minutes)
2. Reduce video frequency
3. Optimize workflow (reduce duration)
4. Use cloud server instead

**Check usage:**
1. Go to **Settings** → **Billing**
2. View **Actions** usage
3. See minutes used/remaining

---

## Optimization Tips

### Reduce Workflow Time

1. **Cache dependencies:**
   ```yaml
   - uses: actions/setup-python@v5
     with:
       cache: 'pip'  # Already enabled
   ```

2. **Reduce video duration:**
   - Use 15-20 second videos
   - Fewer images per video

3. **Optimize image generation:**
   - Lower resolution
   - Fewer images

### Reduce Minutes Usage

1. **Limit video frequency:**
   - 2 videos/day instead of 3
   - Every 12 hours instead of 8

2. **Use manual triggers:**
   - Generate on-demand
   - No scheduled runs

3. **Optimize workflow:**
   - Remove unnecessary steps
   - Combine operations

---

## Advanced Configuration

### Multiple Schedules

Run different workflows at different times:

```yaml
# Morning workflow (1 video)
- cron: '0 9 * * *'

# Afternoon workflow (1 video)
- cron: '0 15 * * *'

# Evening workflow (1 video)
- cron: '0 21 * * *'
```

### Conditional Execution

Run only on specific days:

```yaml
schedule:
  # Monday to Friday only
  - cron: '0 9 * * 1-5'
  
  # Weekends only
  - cron: '0 9 * * 0,6'
```

### Matrix Strategy

Generate multiple videos in parallel:

```yaml
jobs:
  generate-videos:
    strategy:
      matrix:
        topic: ['topic1', 'topic2', 'topic3']
    steps:
      - name: Generate video
        run: python main.py "${{ matrix.topic }}"
```

---

## Security Best Practices

### 1. Never Commit Secrets

Add to `.gitignore`:
```
.env
*.json
*.pickle
youtube_token*
```

### 2. Use Private Repository

For sensitive projects:
- Make repository private
- Accept paid Actions minutes
- Better security

### 3. Limit Workflow Permissions

In workflow file:
```yaml
permissions:
  contents: read
```

### 4. Rotate Secrets

- Change API keys monthly
- Update YouTube token weekly
- Monitor for unauthorized access

### 5. Review Workflow Logs

- Check for exposed secrets
- Monitor API usage
- Watch for errors

---

## Cost Management

### Free Tier (2,000 minutes/month)

**Calculation:**
- Each video: ~5 minutes
- Videos per month: 2,000 ÷ 5 = 400 videos
- Videos per day: 400 ÷ 30 = 13 videos/day

**Recommendation:** Limit to 3-5 videos/day for safety margin

### Paid Plans

| Plan | Minutes/Month | Cost | Videos/Month |
|------|---------------|------|--------------|
| Free | 2,000 | $0 | ~400 |
| Pro | 3,000 | $4 | ~600 |
| Team | 10,000 | $21 | ~2,000 |

### Monitor Usage

1. Go to **Settings** → **Billing**
2. Click **Actions**
3. View usage chart
4. Set spending limit (optional)

---

## Migration to Cloud Server

If GitHub Actions doesn't meet your needs:

### When to Migrate

- Need precise scheduling
- High volume (>10 videos/day)
- Consistent performance
- Long-term automation

### How to Migrate

1. Follow `HOSTING_GUIDE.md`
2. Choose cloud platform
3. Deploy using `deploy.sh`
4. Disable GitHub Actions:
   ```yaml
   # Comment out schedule in daily-videos.yml
   # schedule:
   #   - cron: '0 9 * * *'
   ```

---

## FAQ

### Q: Can I use private repository?

**A:** Yes, but it uses paid Actions minutes. Free tier includes 2,000 minutes/month for private repos.

### Q: How accurate is the scheduling?

**A:** GitHub Actions can delay by 3-10 minutes during high load. Not suitable for precise timing.

### Q: Can I run more than 3 videos per day?

**A:** Yes, but watch your minutes usage. 10 videos/day = ~1,500 minutes/month.

### Q: What if YouTube token expires?

**A:** Download the token artifact from workflow run and update the secret.

### Q: Can I test without uploading to YouTube?

**A:** Yes, use manual workflow and set "Upload to YouTube" to `false`.

### Q: How do I stop the automation?

**A:** Disable the workflow:
1. Go to **Actions** tab
2. Click **Daily Video Automation**
3. Click **⋯** → **Disable workflow**

---

## Quick Reference

### Useful Commands

```bash
# Push code
git add .
git commit -m "Update"
git push

# Encode YouTube token
base64 youtube_token.pickle > youtube_token_base64.txt

# Test locally
python main.py "test topic" --duration 20

# View git status
git status

# View git log
git log --oneline
```

### Workflow Files

- `daily-videos.yml` - Scheduled automation (3x daily)
- `manual-video.yml` - Manual video generation
- `test-setup.yml` - Test environment setup

### Important URLs

- Repository: `https://github.com/YOUR_USERNAME/youtube-shorts-automation`
- Actions: `https://github.com/YOUR_USERNAME/youtube-shorts-automation/actions`
- Settings: `https://github.com/YOUR_USERNAME/youtube-shorts-automation/settings`
- Secrets: `https://github.com/YOUR_USERNAME/youtube-shorts-automation/settings/secrets/actions`

---

## Success Checklist

After setup, verify:

- [ ] Repository created and code pushed
- [ ] All secrets added correctly
- [ ] Test workflow passes ✓
- [ ] Manual video generation works
- [ ] Video uploaded to YouTube
- [ ] Scheduled workflows enabled
- [ ] Timezone configured correctly
- [ ] Monitoring setup
- [ ] Usage tracking enabled

---

## Next Steps

1. ✅ Complete setup above
2. ✅ Test manual video generation
3. ✅ Verify YouTube upload
4. ✅ Enable scheduled workflows
5. ✅ Monitor first few runs
6. ✅ Adjust schedule if needed
7. ✅ Optimize for your needs

---

**Your automation is now running on GitHub Actions!** 🎉

Videos will be posted automatically at your scheduled times (with 3-10 minute delays).

Check your YouTube channel and workflow runs to monitor progress.

# External Scheduling Guide - Bypass GitHub Actions Delays

GitHub Actions scheduled workflows can be delayed by 3-15 minutes during high load. This guide shows you how to use external services for precise timing.

---

## Problem: GitHub Actions Delays

**Issue:** GitHub Actions adds scheduled workflows to a queue, causing delays.

**Impact:**
- Video scheduled for 6:00 AM might run at 6:08 AM
- Delays vary from 3-15 minutes
- More common during peak hours (US business hours)

**Why:** GitHub Actions free tier has lower priority than paid plans.

---

## Solution 1: Use Cron-Job.org (Recommended - Free)

**Pros:**
- ✅ Free forever
- ✅ Runs at exact time (no delays)
- ✅ Easy to set up (5 minutes)
- ✅ Reliable (99.9% uptime)

### Step 1: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `Cron Job Trigger`
4. Select scopes:
   - ✅ `repo` (all)
   - ✅ `workflow`
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)

### Step 2: Sign Up for Cron-Job.org

1. Go to: https://cron-job.org/en/
2. Click **"Sign up"** (free)
3. Verify your email

### Step 3: Create Cron Jobs

For each video time, create a cron job:

#### Job 1: 6:00 AM IST

1. Click **"Create cronjob"**
2. **Title:** `YouTube Video - 6:00 AM IST`
3. **URL:** 
   ```
   https://api.github.com/repos/YOUR_USERNAME/youtube-shorts-automation/dispatches
   ```
   Replace `YOUR_USERNAME` with your GitHub username
4. **Schedule:** 
   - Minute: `0`
   - Hour: `6`
   - Day: `*`
   - Month: `*`
   - Weekday: `*`
5. **Request method:** `POST`
6. **Request body:**
   ```json
   {
     "event_type": "generate-video"
   }
   ```
7. **Headers:**
   - Click **"Add header"**
   - Name: `Authorization`
   - Value: `Bearer YOUR_GITHUB_TOKEN`
   - Click **"Add header"**
   - Name: `Accept`
   - Value: `application/vnd.github.v3+json`
   - Click **"Add header"**
   - Name: `Content-Type`
   - Value: `application/json`
8. Click **"Create cronjob"**

#### Job 2: 4:00 PM IST

Repeat above with:
- **Title:** `YouTube Video - 4:00 PM IST`
- **Hour:** `16`

#### Job 3: 6:20 PM IST

Repeat above with:
- **Title:** `YouTube Video - 6:20 PM IST`
- **Hour:** `18`
- **Minute:** `20`

#### Job 4: 8:30 PM IST

Repeat above with:
- **Title:** `YouTube Video - 8:30 PM IST`
- **Hour:** `20`
- **Minute:** `30`

### Step 4: Test

1. Click **"Execute now"** on one job
2. Go to your GitHub Actions tab
3. You should see the workflow running immediately!

---

## Solution 2: Use EasyCron (Alternative - Free Tier)

**Pros:**
- ✅ Free tier (25 cron jobs)
- ✅ Good UI
- ✅ Reliable

### Setup:

1. Go to: https://www.easycron.com/
2. Sign up (free)
3. Create cron job with same settings as above

---

## Solution 3: Self-Hosted Cron (Advanced)

If you have a computer/server running 24/7:

### On Windows (PowerShell):

Create a script `trigger-video.ps1`:

```powershell
$token = "YOUR_GITHUB_TOKEN"
$username = "YOUR_USERNAME"
$repo = "youtube-shorts-automation"

$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/vnd.github.v3+json"
    "Content-Type" = "application/json"
}

$body = @{
    "event_type" = "generate-video"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.github.com/repos/$username/$repo/dispatches" -Method Post -Headers $headers -Body $body

Write-Host "Video generation triggered!"
```

Then use Windows Task Scheduler to run at your desired times.

### On Linux/Mac (Bash):

Create a script `trigger-video.sh`:

```bash
#!/bin/bash

TOKEN="YOUR_GITHUB_TOKEN"
USERNAME="YOUR_USERNAME"
REPO="youtube-shorts-automation"

curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d '{"event_type":"generate-video"}' \
  "https://api.github.com/repos/$USERNAME/$REPO/dispatches"

echo "Video generation triggered!"
```

Add to crontab:
```bash
crontab -e
```

Add these lines:
```
0 6 * * * /path/to/trigger-video.sh  # 6:00 AM
0 16 * * * /path/to/trigger-video.sh  # 4:00 PM
20 18 * * * /path/to/trigger-video.sh  # 6:20 PM
30 20 * * * /path/to/trigger-video.sh  # 8:30 PM
```

---

## Solution 4: Alternative Hosting Platforms

### Railway.app (Recommended)

**Pros:**
- ✅ Free tier ($5 credit/month)
- ✅ Better scheduling than GitHub Actions
- ✅ Easy deployment

**Setup:**
1. Sign up at https://railway.app/
2. Connect GitHub repo
3. Add cron jobs in Railway dashboard

### Render.com

**Pros:**
- ✅ Free tier
- ✅ Native cron job support
- ✅ Good for Python apps

**Setup:**
1. Sign up at https://render.com/
2. Create new Cron Job
3. Connect GitHub repo
4. Set schedule

### AWS Lambda + EventBridge

**Pros:**
- ✅ Very cheap (almost free)
- ✅ Extremely reliable
- ✅ Precise timing

**Cons:**
- ❌ More complex setup
- ❌ Requires AWS account

---

## Comparison Table

| Solution | Cost | Reliability | Setup Time | Precision |
|----------|------|-------------|------------|-----------|
| GitHub Actions (current) | Free | Medium | 0 min | ±10 min |
| Cron-Job.org | Free | High | 5 min | ±1 sec |
| EasyCron | Free | High | 5 min | ±1 sec |
| Self-Hosted | Free | High | 15 min | ±1 sec |
| Railway.app | $5/mo | Very High | 10 min | ±1 sec |
| Render.com | Free | High | 10 min | ±1 sec |
| AWS Lambda | ~$0.20/mo | Very High | 30 min | ±1 sec |

---

## Recommendation

**For most users:** Use **Cron-Job.org** (Solution 1)
- Free forever
- 5 minutes to set up
- Runs at exact time
- No delays

**For developers:** Use **Self-Hosted Cron** (Solution 3)
- Complete control
- No external dependencies
- Requires 24/7 computer

**For businesses:** Use **Railway.app** or **AWS Lambda**
- Most reliable
- Professional-grade
- Worth the small cost

---

## Keep GitHub Actions as Backup

Even if you use external scheduling, keep the GitHub Actions schedule as a backup:
- If external service fails, GitHub Actions will still run (with delay)
- Provides redundancy
- No harm in having both

---

## Testing External Triggers

After setting up external triggers, test them:

1. Trigger manually from cron-job.org
2. Go to GitHub Actions tab
3. You should see workflow start within 5 seconds!

---

## Monitoring

### Check if External Trigger Worked:

1. Go to GitHub Actions tab
2. Look for "External Trigger (Webhook)" workflow
3. Check run time - should be within 10 seconds of scheduled time

### If It Doesn't Work:

1. Check GitHub token has correct permissions
2. Verify URL is correct (replace YOUR_USERNAME)
3. Check request body format
4. Look at cron-job.org execution logs

---

## Current Setup

After pushing the new workflow:
- ✅ GitHub Actions schedule (backup, may have delays)
- ✅ External trigger endpoint (instant, no delays)
- ✅ Manual trigger (for testing)

You can use either or both!

---

## Next Steps

1. **Recommended:** Set up Cron-Job.org (5 minutes)
2. Test external trigger
3. Keep GitHub Actions as backup
4. Monitor for a few days
5. Adjust as needed

---

**Questions?** The external trigger workflow is already pushed to your repo. Just set up the cron jobs and you're done!

# Cloudflare Worker Setup - Precise Scheduling

Use Cloudflare Workers with Cron Triggers for precise, reliable scheduling (no GitHub Actions delays!)

---

## Why Cloudflare Workers?

- ✅ **Precise timing** - Runs at exact scheduled time (±1 second)
- ✅ **Free tier** - 100,000 requests/day free
- ✅ **Reliable** - Cloudflare's global network
- ✅ **No delays** - Unlike GitHub Actions scheduled workflows
- ✅ **Easy to manage** - Simple dashboard

---

## Prerequisites

1. Cloudflare account (you already have one!)
2. GitHub Personal Access Token
3. Node.js installed (for deployment)

---

## Step 1: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. **Note:** `Cloudflare Worker Trigger`
4. **Expiration:** `No expiration` (or 1 year)
5. Select scopes:
   - ✅ `repo` (all)
   - ✅ `workflow`
6. Click **"Generate token"**
7. **Copy the token** (starts with `ghp_`)

Save it somewhere safe!

---

## Step 2: Install Wrangler CLI

Open PowerShell and run:

```powershell
npm install -g wrangler
```

Verify installation:
```powershell
wrangler --version
```

---

## Step 3: Login to Cloudflare

```powershell
wrangler login
```

This will open a browser window. Log in to your Cloudflare account and authorize Wrangler.

---

## Step 4: Navigate to Worker Directory

```powershell
cd cloudflare-worker
```

---

## Step 5: Install Dependencies

```powershell
npm install
```

---

## Step 6: Set Environment Variables (Secrets)

Set your GitHub token:
```powershell
wrangler secret put GITHUB_TOKEN
```

When prompted, paste your GitHub token (from Step 1) and press Enter.

Set your GitHub repository:
```powershell
wrangler secret put GITHUB_REPO
```

When prompted, enter: `rajnishkumar13500/youtube-shorts-automation` and press Enter.

---

## Step 7: Deploy Worker

```powershell
wrangler deploy
```

You should see:
```
✨ Success! Uploaded worker 'youtube-shorts-scheduler'
🌎 https://youtube-shorts-scheduler.YOUR_SUBDOMAIN.workers.dev
```

Copy the URL - this is your worker endpoint!

---

## Step 8: Verify Deployment

Test the health endpoint:
```powershell
curl https://youtube-shorts-scheduler.YOUR_SUBDOMAIN.workers.dev/health
```

You should see:
```json
{
  "status": "ok",
  "message": "YouTube Shorts Automation Worker is running",
  "timestamp": "2024-03-24T..."
}
```

---

## Step 9: Test Manual Trigger

Test triggering a video generation:

```powershell
curl -X POST https://youtube-shorts-scheduler.YOUR_SUBDOMAIN.workers.dev/trigger
```

Then check GitHub Actions:
https://github.com/rajnishkumar13500/youtube-shorts-automation/actions

You should see "External Trigger (Webhook)" workflow running!

---

## Step 10: Verify Cron Triggers

1. Go to Cloudflare Dashboard: https://dash.cloudflare.com/
2. Click **Workers & Pages**
3. Click **youtube-shorts-scheduler**
4. Click **Triggers** tab
5. You should see 4 cron triggers:
   - `0 6 * * *` - 6:00 AM IST
   - `30 10 * * *` - 4:00 PM IST
   - `50 12 * * *` - 6:20 PM IST
   - `0 15 * * *` - 8:30 PM IST

---

## Cron Schedule Explained

The worker is configured to run 4 times per day:

| Time (IST) | Time (UTC) | Cron Expression | Purpose |
|------------|------------|-----------------|---------|
| 6:00 AM    | 12:30 AM   | `0 6 * * *`     | Morning video |
| 4:00 PM    | 10:30 AM   | `30 10 * * *`   | Afternoon video |
| 6:20 PM    | 12:50 PM   | `50 12 * * *`   | Evening video |
| 8:30 PM    | 3:00 PM    | `0 15 * * *`    | Night video |

**Note:** Cron times in `wrangler.toml` are in UTC, but I've already converted them for you!

---

## How It Works

1. **Cloudflare Cron Trigger** fires at scheduled time (precise!)
2. **Worker** receives the trigger
3. **Worker** calls GitHub API to trigger workflow
4. **GitHub Actions** starts "External Trigger (Webhook)" workflow
5. **Video generation** happens (2-3 minutes)
6. **YouTube upload** completes
7. **Google Sheets** updates with video URL

---

## Monitoring

### View Worker Logs

1. Go to Cloudflare Dashboard
2. Click **Workers & Pages**
3. Click **youtube-shorts-scheduler**
4. Click **Logs** tab (real-time logs)

### View GitHub Actions

https://github.com/rajnishkumar13500/youtube-shorts-automation/actions

Look for "External Trigger (Webhook)" workflows.

### Check Execution History

In Cloudflare Dashboard:
- **Metrics** tab shows request count, errors, CPU time
- **Logs** tab shows real-time execution logs

---

## Troubleshooting

### Worker deployed but not triggering

1. Check secrets are set:
   ```powershell
   wrangler secret list
   ```
   Should show: `GITHUB_TOKEN`, `GITHUB_REPO`

2. Check cron triggers in Cloudflare Dashboard

3. Test manual trigger:
   ```powershell
   curl -X POST https://youtube-shorts-scheduler.YOUR_SUBDOMAIN.workers.dev/trigger
   ```

### GitHub workflow not starting

1. Verify GitHub token has `repo` and `workflow` permissions
2. Check token hasn't expired
3. Verify repository name is correct: `rajnishkumar13500/youtube-shorts-automation`

### Cron not firing

1. Wait for next scheduled time (cron triggers run at exact times)
2. Check Cloudflare Dashboard > Workers > Logs
3. Verify cron expressions in `wrangler.toml`

---

## Updating Schedule

To change the schedule:

1. Edit `cloudflare-worker/wrangler.toml`
2. Update the `crons` array
3. Redeploy:
   ```powershell
   cd cloudflare-worker
   wrangler deploy
   ```

Example - 3 videos per day:
```toml
crons = [
  "30 3 * * *",   # 9:00 AM IST
  "30 9 * * *",   # 3:00 PM IST
  "30 15 * * *"   # 9:00 PM IST
]
```

---

## Cost

**Cloudflare Workers Free Tier:**
- 100,000 requests/day
- 10ms CPU time per request
- Unlimited cron triggers

**Your usage:**
- 4 cron triggers/day = 120/month
- Well within free tier! ✅

---

## Advantages Over GitHub Actions

| Feature | GitHub Actions | Cloudflare Workers |
|---------|---------------|-------------------|
| Timing precision | ±10 minutes | ±1 second |
| Reliability | Medium | Very High |
| Free tier | Yes | Yes |
| Setup complexity | Low | Medium |
| Monitoring | Good | Excellent |

---

## Commands Reference

```powershell
# Login to Cloudflare
wrangler login

# Deploy worker
cd cloudflare-worker
wrangler deploy

# Set secrets
wrangler secret put GITHUB_TOKEN
wrangler secret put GITHUB_REPO

# List secrets
wrangler secret list

# View logs (real-time)
wrangler tail

# Test locally
wrangler dev

# Delete worker (if needed)
wrangler delete
```

---

## Current Setup

After deployment:
- ✅ 4 videos per day
- ✅ Precise timing (no delays)
- ✅ Times: 6:00 AM, 4:00 PM, 6:20 PM, 8:30 PM IST
- ✅ Automatic, reliable, free
- ✅ Easy to monitor and manage

---

## Next Steps

1. ✅ Deploy worker (Step 2-7)
2. ✅ Test manual trigger (Step 9)
3. ✅ Wait for first scheduled run
4. ✅ Monitor in Cloudflare Dashboard
5. ✅ Check GitHub Actions for workflow runs

---

## Support

**Cloudflare Workers Docs:**
https://developers.cloudflare.com/workers/

**Wrangler CLI Docs:**
https://developers.cloudflare.com/workers/wrangler/

**Cron Triggers Docs:**
https://developers.cloudflare.com/workers/configuration/cron-triggers/

---

**Ready?** Start with Step 2 and follow through. Takes about 10 minutes!

Your videos will post at EXACT times with Cloudflare Workers! 🚀

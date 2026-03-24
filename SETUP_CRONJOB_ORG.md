# Setup Cron-Job.org - Step by Step

Follow these steps to set up precise scheduling with cron-job.org (no more GitHub delays!)

---

## Step 1: Create GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. **Note:** `Cron Job Trigger`
4. **Expiration:** `No expiration` (or 1 year)
5. Select these scopes:
   - ✅ Check `repo` (this will check all sub-items)
   - ✅ Check `workflow`
6. Scroll down and click **"Generate token"**
7. **IMPORTANT:** Copy the token immediately (starts with `ghp_`)
   - Save it somewhere safe
   - You won't be able to see it again!

Example token: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## Step 2: Sign Up for Cron-Job.org

1. Go to: https://cron-job.org/en/
2. Click **"Sign up"** (top right)
3. Fill in:
   - Email address
   - Password
   - Accept terms
4. Click **"Sign up"**
5. Check your email and verify your account
6. Log in to cron-job.org

---

## Step 3: Get Your GitHub Repository URL

Your repository dispatch URL is:
```
https://api.github.com/repos/rajnishkumar13500/youtube-shorts-automation/dispatches
```

(I've already filled in your username from the git remote)

---

## Step 4: Create Cron Job #1 - 6:00 AM IST

1. In cron-job.org dashboard, click **"Create cronjob"**

2. **Title:** `YouTube Video - 6:00 AM IST`

3. **Address (URL):**
   ```
   https://api.github.com/repos/rajnishkumar13500/youtube-shorts-automation/dispatches
   ```

4. **Schedule:**
   - Click **"Every day"**
   - **Hour:** `6`
   - **Minute:** `0`
   - Leave other fields as default

5. **Advanced settings** (click to expand):
   - **Request method:** Select `POST`
   - **Request body:**
     ```json
     {"event_type":"generate-video"}
     ```
   
6. **Headers** (click "Add header" for each):
   
   Header 1:
   - **Name:** `Authorization`
   - **Value:** `Bearer ghp_YOUR_TOKEN_HERE`
     (Replace `ghp_YOUR_TOKEN_HERE` with your actual GitHub token from Step 1)
   
   Header 2:
   - **Name:** `Accept`
   - **Value:** `application/vnd.github.v3+json`
   
   Header 3:
   - **Name:** `Content-Type`
   - **Value:** `application/json`

7. **Enabled:** Make sure it's checked ✅

8. Click **"Create cronjob"**

---

## Step 5: Create Cron Job #2 - 4:00 PM IST

Repeat Step 4 with these changes:
- **Title:** `YouTube Video - 4:00 PM IST`
- **Hour:** `16`
- **Minute:** `0`
- Everything else stays the same

---

## Step 6: Create Cron Job #3 - 6:20 PM IST

Repeat Step 4 with these changes:
- **Title:** `YouTube Video - 6:20 PM IST`
- **Hour:** `18`
- **Minute:** `20`
- Everything else stays the same

---

## Step 7: Create Cron Job #4 - 8:30 PM IST

Repeat Step 4 with these changes:
- **Title:** `YouTube Video - 8:30 PM IST`
- **Hour:** `20`
- **Minute:** `30`
- Everything else stays the same

---

## Step 8: Test One Cron Job

1. In your cron-job.org dashboard, find one of your cron jobs
2. Click the **"Execute now"** button (play icon ▶️)
3. Wait 5-10 seconds
4. Go to your GitHub repository: https://github.com/rajnishkumar13500/youtube-shorts-automation/actions
5. You should see **"External Trigger (Webhook)"** workflow running!
6. If it works, you're all set! ✅

---

## Troubleshooting

### If the test doesn't work:

1. **Check the execution log in cron-job.org:**
   - Click on the cron job
   - Look at "Execution history"
   - Check for error messages

2. **Common issues:**
   - ❌ **401 Unauthorized:** GitHub token is wrong or missing `workflow` permission
   - ❌ **404 Not Found:** Repository URL is wrong
   - ❌ **422 Unprocessable:** Request body format is wrong

3. **Verify your settings:**
   - GitHub token starts with `ghp_`
   - Authorization header: `Bearer ghp_YOUR_TOKEN` (with space after Bearer)
   - Request body is exactly: `{"event_type":"generate-video"}`
   - All 3 headers are added

---

## What Happens Now?

Starting from the next scheduled time:

1. **Cron-job.org** triggers your workflow at EXACT time (no delays!)
2. **GitHub Actions** receives the trigger and starts immediately
3. **Video generation** happens (2-3 minutes)
4. **YouTube upload** completes
5. **Google Sheets** updates with video URL

All at the precise time you scheduled! 🎯

---

## Monitoring

### Check if it's working:

1. Go to: https://github.com/rajnishkumar13500/youtube-shorts-automation/actions
2. Look for "External Trigger (Webhook)" workflows
3. Check the start time - should be within 10 seconds of scheduled time!

### Cron-job.org dashboard:

- Shows execution history
- Success/failure status
- Response codes
- Execution time

---

## Summary

You now have:
- ✅ 4 cron jobs set up on cron-job.org
- ✅ Videos will post at EXACT times (no delays)
- ✅ 6:00 AM, 4:00 PM, 6:20 PM, 8:30 PM IST
- ✅ Automatic, reliable, free forever

---

## Quick Reference

**Your cron jobs:**
1. 6:00 AM IST - Daily
2. 4:00 PM IST - Daily  
3. 6:20 PM IST - Daily
4. 8:30 PM IST - Daily

**GitHub Actions URL:**
```
https://github.com/rajnishkumar13500/youtube-shorts-automation/actions
```

**Cron-job.org dashboard:**
```
https://cron-job.org/en/members/jobs/
```

---

## Need Help?

If you get stuck:
1. Check the execution log in cron-job.org
2. Verify your GitHub token has `repo` and `workflow` permissions
3. Make sure all 3 headers are added correctly
4. Test with "Execute now" button

---

**Ready?** Start with Step 1 and work your way through. It takes about 10 minutes total!

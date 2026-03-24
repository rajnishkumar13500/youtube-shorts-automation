# Schedule Configuration - 4 Videos Daily

Your automation is configured to post 4 videos per day automatically!

---

## Current Schedule (India IST)

**File:** `.github/workflows/daily-videos.yml`

**Posting times:**
- Video 1: 6:00 AM IST (12:30 AM UTC)
- Video 2: 4:00 PM IST (10:30 AM UTC)
- Video 3: 6:20 PM IST (12:50 PM UTC)
- Video 4: 8:30 PM IST (3:00 PM UTC)

---

## Schedule Details

```yaml
schedule:
  # 6:00 AM IST = 12:30 AM UTC
  - cron: '30 0 * * *'
  # 4:00 PM IST = 10:30 AM UTC
  - cron: '30 10 * * *'
  # 6:20 PM IST = 12:50 PM UTC
  - cron: '50 12 * * *'
  # 8:30 PM IST = 3:00 PM UTC
  - cron: '0 15 * * *'
```

---

## Adjust for Your Timezone

### India (IST = UTC+5:30)

Current configuration (4 videos per day):

```yaml
schedule:
  # 6:00 AM IST = 12:30 AM UTC
  - cron: '30 0 * * *'
  # 4:00 PM IST = 10:30 AM UTC
  - cron: '30 10 * * *'
  # 6:20 PM IST = 12:50 PM UTC
  - cron: '50 12 * * *'
  # 8:30 PM IST = 3:00 PM UTC
  - cron: '0 15 * * *'
```

If you want different times (e.g., 9 AM, 3 PM, 9 PM IST):

```yaml
schedule:
  # 9:00 AM IST = 3:30 AM UTC
  - cron: '30 3 * * *'
  # 3:00 PM IST = 9:30 AM UTC
  - cron: '30 9 * * *'
  # 9:00 PM IST = 3:30 PM UTC
  - cron: '30 15 * * *'
```

### US Eastern (EST = UTC-5)

If you want videos at 9 AM, 3 PM, 9 PM EST:

```yaml
schedule:
  # 9:00 AM EST = 2:00 PM UTC
  - cron: '0 14 * * *'
  # 3:00 PM EST = 8:00 PM UTC
  - cron: '0 20 * * *'
  # 9:00 PM EST = 2:00 AM UTC (next day)
  - cron: '0 2 * * *'
```

### UK (GMT = UTC+0)

If you want videos at 9 AM, 3 PM, 9 PM GMT:

```yaml
schedule:
  # 9:00 AM GMT = 9:00 AM UTC
  - cron: '0 9 * * *'
  # 3:00 PM GMT = 3:00 PM UTC
  - cron: '0 15 * * *'
  # 9:00 PM GMT = 9:00 PM UTC
  - cron: '0 21 * * *'
```

---

## How to Change Schedule

### Step 1: Edit the Workflow File

Open `.github/workflows/daily-videos.yml` and find this section:

```yaml
schedule:
  # 9:00 AM UTC (adjust for your timezone)
  - cron: '0 9 * * *'
  # 3:00 PM UTC
  - cron: '0 15 * * *'
  # 9:00 PM UTC
  - cron: '0 21 * * *'
```

### Step 2: Update Cron Times

Replace with your desired times using the timezone examples above.

### Step 3: Commit and Push

```powershell
git add .github/workflows/daily-videos.yml
git commit -m "Update video posting schedule"
git push
```

---

## Cron Syntax Explained

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday)
│ │ │ │ │
* * * * *
```

**Examples:**
- `0 9 * * *` = Every day at 9:00 AM UTC
- `30 15 * * *` = Every day at 3:30 PM UTC
- `0 */8 * * *` = Every 8 hours
- `0 9 * * 1-5` = Every weekday at 9:00 AM UTC

---

## Timezone Conversion Table

| Your Time | IST (UTC+5:30) | EST (UTC-5) | PST (UTC-8) | GMT (UTC+0) |
|-----------|----------------|-------------|-------------|-------------|
| 9:00 AM   | 3:30 UTC       | 14:00 UTC   | 17:00 UTC   | 9:00 UTC    |
| 3:00 PM   | 9:30 UTC       | 20:00 UTC   | 23:00 UTC   | 15:00 UTC   |
| 9:00 PM   | 15:30 UTC      | 2:00 UTC*   | 5:00 UTC*   | 21:00 UTC   |

*Next day

---

## Important Notes

### GitHub Actions Delays

⚠️ **GitHub Actions may delay scheduled workflows by 3-10 minutes** during high load.

- Your video might post at 9:03 AM instead of 9:00 AM
- This is normal and expected
- Cannot be avoided on free tier

### First Run

The first scheduled run will happen at the next scheduled time after you push the workflow.

### Manual Testing

You can test the workflow manually:
1. Go to **Actions** tab
2. Click **"Daily Video Automation"**
3. Click **"Run workflow"**
4. Leave topic empty (uses Google Sheets)
5. Click **"Run workflow"**

---

## Change Frequency

### Post More Videos

Want 6 videos per day? Add more cron schedules:

```yaml
schedule:
  - cron: '0 6 * * *'   # 6 AM
  - cron: '0 9 * * *'   # 9 AM
  - cron: '0 12 * * *'  # 12 PM
  - cron: '0 15 * * *'  # 3 PM
  - cron: '0 18 * * *'  # 6 PM
  - cron: '0 21 * * *'  # 9 PM
```

### Post Less Videos

Want 1 video per day? Keep only one:

```yaml
schedule:
  - cron: '0 9 * * *'   # 9 AM only
```

### Post Every X Hours

Want video every 8 hours?

```yaml
schedule:
  - cron: '0 */8 * * *'  # Every 8 hours
```

---

## Verify Schedule

After pushing changes:

1. Go to **Actions** tab
2. Click **"Daily Video Automation"**
3. You'll see "This workflow has a workflow_dispatch event trigger"
4. Next scheduled run will show in the workflow

---

## Disable Scheduled Posts

To temporarily disable automatic posting:

### Option 1: Comment Out Schedule

```yaml
# schedule:
#   - cron: '0 9 * * *'
#   - cron: '0 15 * * *'
#   - cron: '0 21 * * *'
```

### Option 2: Disable Workflow

1. Go to **Actions** tab
2. Click **"Daily Video Automation"**
3. Click **"⋯"** (three dots)
4. Click **"Disable workflow"**

---

## Monitor Scheduled Runs

### View Past Runs

1. Go to **Actions** tab
2. Click **"Daily Video Automation"**
3. See all past runs with timestamps

### Check Next Run

GitHub doesn't show next scheduled run time, but it will run at your configured cron times.

### View Logs

1. Click on any workflow run
2. Click job name
3. Expand steps to see detailed logs

---

## Current Configuration

Your current setup:
- ✅ 4 videos per day
- ✅ Times: 6:00 AM, 4:00 PM, 6:20 PM, 8:30 PM IST
- ✅ Pulls topics from Google Sheets
- ✅ Uploads to YouTube automatically
- ✅ Updates status in Google Sheets

**Everything is ready!** Videos will start posting automatically at the scheduled times.

---

## Content Planning

With 4 videos per day:
- 4 videos/day × 30 days = 120 videos/month
- 4 videos/day × 365 days = 1,460 videos/year

Your Google Sheets has 690 topics = 172.5 days of content (almost 6 months!)

---

## Quick Reference

**To change schedule:**
1. Edit `.github/workflows/daily-videos.yml`
2. Update cron times
3. `git add .github/workflows/daily-videos.yml`
4. `git commit -m "Update schedule"`
5. `git push`

**To test manually:**
1. Go to Actions tab
2. Run "Daily Video Automation" workflow
3. Leave topic empty

**To disable:**
1. Actions tab → Daily Video Automation
2. Click ⋯ → Disable workflow

---

**Your automation is live!** 🎉

Videos will post automatically 4 times per day from your Google Sheets topics.

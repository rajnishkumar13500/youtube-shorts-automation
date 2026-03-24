# Complete GitHub Actions Setup - Do This Now!

Follow these steps in order to complete your setup.

---

## Step 1: Add GitHub Secrets (5 minutes)

Go to your GitHub repository and add these secrets:

**URL:** https://github.com/YOUR_USERNAME/youtube-shorts-automation/settings/secrets/actions

Click **"New repository secret"** for each one:

### Required Secrets (Copy from your .env file)

| Secret Name | Where to Find Value |
|------------|---------------------|
| `GROQ_API_KEY` | Copy from your `.env` file |
| `ELEVENLABS_API_KEY` | Copy from your `.env` file |
| `ELEVENLABS_API_KEY_2` | Copy from your `.env` file |
| `ELEVENLABS_API_KEY_3` | Copy from your `.env` file |
| `CLOUDFLARE_ACCOUNT_ID` | Copy from your `.env` file |
| `CLOUDFLARE_API_TOKEN` | Copy from your `.env` file |
| `GOOGLE_SHEETS_ID` | Copy from your `.env` file |

### JSON Credentials (Need special handling)

#### GOOGLE_SHEETS_CREDENTIALS

```powershell
# Copy entire JSON file content
Get-Content youtube-automation-491110-613db1f9bbb0.json | Out-String
```

Copy the output and paste as secret value.

#### YOUTUBE_CLIENT_SECRETS

```powershell
# Copy entire JSON file content
Get-Content client_secret_346866923009-ptgobvgfk2a8mmepb0uop05oetdjf4tv.apps.googleusercontent.com.json | Out-String
```

Copy the output and paste as secret value.

---

## Step 2: Authenticate YouTube & Create Token (3 minutes)

We need to authenticate YouTube locally first, then upload the token to GitHub.

### 2a. Test Video Generation Locally

```powershell
# Generate a test video to trigger YouTube authentication
python main.py "drinking water benefits" --duration 20
```

This will:
1. Generate a video
2. Create `youtube_token.pickle` file
3. You'll need to authenticate in browser

### 2b. Encode YouTube Token

After authentication completes:

```powershell
# Encode the token to base64
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) | Out-File -Encoding ASCII youtube_token_base64.txt

# Display the encoded token
Get-Content youtube_token_base64.txt
```

### 2c. Add YOUTUBE_TOKEN Secret

1. Copy the entire output from above
2. Go to GitHub Secrets page
3. Add new secret: `YOUTUBE_TOKEN`
4. Paste the base64 encoded value

---

## Step 3: Populate Google Sheets (2 minutes)

```powershell
# Add 500 topics to your spreadsheet
python populate_spreadsheet.py
```

This will add 500+ health/fitness topics to your Google Sheets.

---

## Step 4: Test GitHub Actions (5 minutes)

### 4a. Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **"Actions"** tab
3. Click **"I understand my workflows, go ahead and enable them"**

### 4b. Run Test Workflow

1. Click **"Test Setup"** workflow
2. Click **"Run workflow"** dropdown
3. Click **"Run workflow"** button
4. Wait 2-3 minutes
5. Check for green checkmark ✓

### 4c. Generate Test Video

1. Click **"Generate Single Video (Manual)"** workflow
2. Click **"Run workflow"** dropdown
3. Enter:
   - **Topic:** `drinking water benefits`
   - **Duration:** `20`
   - **Upload to YouTube:** `true`
4. Click **"Run workflow"** button
5. Wait 5-10 minutes
6. Check your YouTube channel!

---

## Step 5: Enable Scheduled Automation (1 minute)

The scheduled workflow is already configured! It will automatically run at:
- 9:00 AM UTC
- 3:00 PM UTC
- 9:00 PM UTC

### Adjust for Your Timezone (Optional)

If you want to change the times, edit `.github/workflows/daily-videos.yml`:

For India (IST = UTC+5:30):
```yaml
schedule:
  # 9:00 AM IST = 3:30 AM UTC
  - cron: '30 3 * * *'
  # 3:00 PM IST = 9:30 AM UTC
  - cron: '30 9 * * *'
  # 9:00 PM IST = 3:30 PM UTC
  - cron: '30 15 * * *'
```

Then commit and push:
```powershell
git add .github/workflows/daily-videos.yml
git commit -m "Adjust schedule for IST timezone"
git push
```

---

## Quick Command Summary

```powershell
# Step 1: Copy JSON credentials
Get-Content youtube-automation-491110-613db1f9bbb0.json | Out-String
Get-Content client_secret_346866923009-ptgobvgfk2a8mmepb0uop05oetdjf4tv.apps.googleusercontent.com.json | Out-String

# Step 2: Generate test video & authenticate
python main.py "drinking water benefits" --duration 20

# Step 2b: Encode YouTube token
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) | Out-File -Encoding ASCII youtube_token_base64.txt
Get-Content youtube_token_base64.txt

# Step 3: Populate spreadsheet
python populate_spreadsheet.py
```

---

## Verification Checklist

After completing all steps:

- [ ] All 9 secrets added to GitHub
- [ ] Test Setup workflow passes ✓
- [ ] Manual video workflow generates video
- [ ] Video uploads to YouTube successfully
- [ ] Google Sheets has 500 topics
- [ ] Scheduled workflows enabled
- [ ] First scheduled video posts successfully

---

## Troubleshooting

### "Secret not found" error

Make sure secret names are EXACTLY:
- `GROQ_API_KEY` (not groq_api_key)
- `ELEVENLABS_API_KEY` (not elevenlabs_api_key)
- etc.

### YouTube authentication fails

```powershell
# Re-authenticate locally
python setup_youtube_account.py
python main.py "test" --duration 20

# Re-encode token
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) | Out-File -Encoding ASCII youtube_token_base64.txt

# Update YOUTUBE_TOKEN secret with new value
```

### Video generation fails

Check workflow logs:
1. Go to Actions tab
2. Click failed workflow
3. Click job name
4. Expand steps to see error

Common issues:
- API key invalid → Update secret
- Quota exceeded → Wait or use fallback keys
- FFmpeg error → Check video generation code

---

## What Happens Next?

After setup completes:

1. **Scheduled workflows run automatically** at 9 AM, 3 PM, 9 PM UTC
2. **Videos are generated** from Google Sheets topics
3. **Videos are uploaded** to YouTube automatically
4. **Status is updated** in Google Sheets
5. **Logs are saved** as artifacts in GitHub Actions

---

## Monitoring

### View Workflow Runs

1. Go to **Actions** tab
2. See all workflow runs
3. Green ✓ = Success, Red ✗ = Failed

### View Logs

1. Click on workflow run
2. Click job name
3. Expand steps to see detailed logs

### Download Logs

1. Scroll to bottom of workflow run
2. Click **logs-XXX** artifact
3. Download and extract

---

## Next Steps

1. ✅ Complete all steps above
2. ✅ Verify first video posts successfully
3. ✅ Monitor for 24 hours
4. ✅ Adjust settings if needed
5. ✅ Scale up if working well

---

**Ready? Start with Step 1!**

Go to: https://github.com/YOUR_USERNAME/youtube-shorts-automation/settings/secrets/actions

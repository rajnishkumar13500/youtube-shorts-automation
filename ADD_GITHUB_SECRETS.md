# How to Add GitHub Secrets

Your API keys and credentials should NEVER be committed to GitHub. Instead, add them as secrets.

## Step 1: Go to GitHub Secrets Page

https://github.com/YOUR_USERNAME/youtube-shorts-automation/settings/secrets/actions

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 2: Add Each Secret

Click **"New repository secret"** and add these 10 secrets:

### From Your .env File

Copy the values from your local `.env` file:

1. **GROQ_API_KEY** - Your Groq API key
2. **ELEVENLABS_API_KEY** - Your ElevenLabs API key
3. **ELEVENLABS_API_KEY_2** - Your second ElevenLabs API key
4. **ELEVENLABS_API_KEY_3** - Your third ElevenLabs API key
5. **CLOUDFLARE_ACCOUNT_ID** - Your Cloudflare account ID
6. **CLOUDFLARE_API_TOKEN** - Your Cloudflare API token
7. **GOOGLE_SHEETS_ID** - Your Google Sheets spreadsheet ID

### JSON Credentials

#### 8. GOOGLE_SHEETS_CREDENTIALS

Run this command to copy the JSON:
```powershell
Get-Content youtube-automation-491110-613db1f9bbb0.json | Out-String
```

Copy the entire output and paste as the secret value.

#### 9. YOUTUBE_CLIENT_SECRETS

Run this command to copy the JSON:
```powershell
Get-Content client_secret_*.json | Out-String
```

Copy the entire output and paste as the secret value.

#### 10. YOUTUBE_TOKEN

First, authenticate YouTube locally:
```powershell
python main.py "test topic" --duration 20
```

Then encode the token:
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) | Out-File -Encoding ASCII youtube_token_base64.txt
Get-Content youtube_token_base64.txt
```

Copy the output and paste as the secret value.

## Step 3: Verify

After adding all 10 secrets, you should see them listed on the secrets page (values are hidden for security).

## Step 4: Test

Go to the Actions tab and run the "Test Setup" workflow to verify everything works.

---

**IMPORTANT:** Never commit files containing API keys or secrets to GitHub!

# Fix YouTube "Access Blocked" Error

## Problem

You're seeing: "Access blocked: YouTube Shorts Automation has not completed the Google verification process"

## Solution: Add Yourself as Test User

You don't need to verify your app with Google. Just add yourself as a test user!

---

## Step-by-Step Fix

### 1. Go to Google Cloud Console

Open: https://console.cloud.google.com/

### 2. Select Your Project

Click the project dropdown at the top and select your YouTube automation project.

### 3. Go to OAuth Consent Screen

1. Click the hamburger menu (☰) on the left
2. Navigate to: **APIs & Services** > **OAuth consent screen**
3. Or direct link: https://console.cloud.google.com/apis/credentials/consent

### 4. Add Test Users

1. Scroll down to **"Test users"** section
2. Click **"+ ADD USERS"** button
3. Enter your Gmail/Google account email (the one you want to use for YouTube)
4. Click **"SAVE"**

Example:
```
youremail@gmail.com
```

### 5. Save Changes

Click **"SAVE AND CONTINUE"** at the bottom.

### 6. Try Authentication Again

Now run the authentication script again:

```powershell
python authenticate_youtube.py
```

This time it should work!

---

## Alternative: Publish App (Not Recommended for Personal Use)

If you want anyone to use your app, you need to publish it:

1. Go to OAuth consent screen
2. Click **"PUBLISH APP"**
3. Click **"CONFIRM"**

**Note:** For personal automation, just use test users. It's simpler and works perfectly.

---

## Verification Status

### Test Mode (Recommended for Personal Use)
- ✅ Works for test users only
- ✅ No verification needed
- ✅ Up to 100 test users
- ✅ Perfect for personal automation

### Published Mode (For Public Apps)
- ⚠️ Requires Google verification
- ⚠️ Takes weeks to approve
- ⚠️ Requires privacy policy
- ⚠️ Only needed for public apps

---

## Common Issues

### "Email not added as test user"

**Solution:** Make sure you added the EXACT email address you're trying to login with.

### "App is in testing mode"

**Solution:** This is normal! Just make sure you're logged in with a test user email.

### "This app hasn't been verified"

**Solution:** Click **"Advanced"** → **"Go to YouTube Shorts Automation (unsafe)"**

This is safe because it's YOUR app.

---

## Quick Fix Commands

After adding yourself as test user:

```powershell
# Try authentication again
python authenticate_youtube.py

# If successful, encode token
[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) | Out-File -Encoding ASCII youtube_token_base64.txt

# View encoded token
Get-Content youtube_token_base64.txt
```

---

## Screenshots Guide

### Step 1: OAuth Consent Screen
```
Google Cloud Console
└── APIs & Services
    └── OAuth consent screen
        └── Test users section
            └── + ADD USERS button
```

### Step 2: Add Email
```
Enter email addresses:
┌─────────────────────────────┐
│ youremail@gmail.com         │
└─────────────────────────────┘
[SAVE]
```

### Step 3: Verify
```
Test users:
✓ youremail@gmail.com
```

---

## After Adding Test User

1. ✅ Run `python authenticate_youtube.py`
2. ✅ Browser opens
3. ✅ Login with test user email
4. ✅ Click "Advanced" if you see warning
5. ✅ Click "Go to YouTube Shorts Automation (unsafe)"
6. ✅ Grant permissions
7. ✅ Authentication complete!

---

## Important Notes

- You can add up to 100 test users
- Test users can use your app without verification
- Your app stays in "Testing" mode - this is fine!
- No need to publish or verify for personal use
- Test users never expire

---

## Next Steps

After authentication succeeds:

1. ✅ `youtube_token.pickle` file created
2. ✅ Encode token for GitHub
3. ✅ Add to GitHub Secrets
4. ✅ Test video upload

---

**Need Help?**

If you still see errors:
1. Double-check email is added as test user
2. Make sure you're logged into correct Google account in browser
3. Try incognito/private browsing mode
4. Clear browser cookies for google.com

---

**Ready?** Go add yourself as test user now:

https://console.cloud.google.com/apis/credentials/consent

# 🚀 START HERE - YouTube Shorts Automation

Welcome! This guide will get you started in 5 minutes.

---

## What This Does

Automatically generates and posts YouTube Shorts videos:
- ✅ AI-generated scripts (Groq/Llama)
- ✅ Natural voiceovers (ElevenLabs)
- ✅ AI-generated images (Cloudflare)
- ✅ Synchronized subtitles (Whisper AI)
- ✅ Automatic YouTube upload
- ✅ Scheduled posting (3 videos/day)

---

## Quick Start (Choose One)

### Option 1: GitHub Actions (FREE) ⭐ Recommended

**Cost:** $0/month  
**Setup:** 15 minutes  
**Videos:** ~400/month (free tier)

**Steps:**
1. Read: `PUSH_TO_GITHUB.md` (push code safely)
2. Follow: `GITHUB_ACTIONS_SETUP.md` (complete setup)
3. Done! Videos post automatically

### Option 2: Cloud Server

**Cost:** $12-30/month  
**Setup:** 30-60 minutes  
**Videos:** Unlimited

**Steps:**
1. Read: `DEPLOYMENT_QUICKSTART.md`
2. Run: `./deploy.sh` on your server
3. Done! Videos post automatically

### Option 3: Local Testing

**Cost:** $0  
**Setup:** 10 minutes  
**Videos:** Manual only

**Steps:**
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
python main.py "test topic" --duration 20
```

---

## Documentation Map

### 📚 Getting Started
- **START_HERE.md** ← You are here
- **README.md** - Full project overview
- **PUSH_TO_GITHUB.md** - How to push code safely

### 🤖 GitHub Actions (FREE)
- **GITHUB_ACTIONS_GUIDE.md** - Complete guide
- **GITHUB_ACTIONS_SETUP.md** - Step-by-step setup
- **.github/workflows/** - Workflow files

### ☁️ Cloud Hosting
- **HOSTING_GUIDE.md** - Complete hosting guide
- **DEPLOYMENT_QUICKSTART.md** - Quick deployment
- **deploy.sh** - Automated deployment script

### 🤔 Decision Making
- **CHOOSE_DEPLOYMENT.md** - Compare options

### ⚙️ Configuration
- **.env.example** - Environment template
- **config.py** - System settings
- **requirements.txt** - Dependencies

---

## What You Need

### Required API Keys (All FREE tiers available)

1. **Groq** - Script generation
   - Get: https://console.groq.com/
   - Free: Unlimited (rate limited)

2. **ElevenLabs** - Voice synthesis
   - Get: https://elevenlabs.io/
   - Free: 10,000 characters/month

3. **Cloudflare AI** - Image generation
   - Get: https://dash.cloudflare.com/
   - Free: 10,000 requests/day

4. **Google Sheets** - Topic management
   - Get: https://console.cloud.google.com/
   - Free: Unlimited

5. **YouTube Data API** - Video upload
   - Get: https://console.cloud.google.com/
   - Free: 10,000 quota/day

---

## Recommended Path

### For Beginners (Start Here!)

1. **Week 1:** Setup GitHub Actions (FREE)
   - Follow `PUSH_TO_GITHUB.md`
   - Follow `GITHUB_ACTIONS_SETUP.md`
   - Generate 10-20 test videos

2. **Week 2-4:** Test and optimize
   - Adjust subtitle timing
   - Try different topics
   - Monitor performance

3. **Month 2+:** Scale up
   - If happy with free tier: Continue
   - If need more: Migrate to cloud server

### For Production (High Volume)

1. **Day 1:** Setup cloud server
   - Follow `DEPLOYMENT_QUICKSTART.md`
   - Run `deploy.sh`

2. **Day 2-7:** Test and monitor
   - Verify scheduled posts
   - Check logs
   - Optimize settings

3. **Week 2+:** Scale
   - Add more topics
   - Increase frequency
   - Monitor costs

---

## Quick Commands

### Push to GitHub

```bash
# IMPORTANT: Read PUSH_TO_GITHUB.md first!
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/youtube-shorts-automation.git
git push -u origin main
```

### Test Locally

```bash
# Install dependencies
pip install -r requirements.txt
pip install openai-whisper

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Generate test video
python main.py "drinking water benefits" --duration 20

# Populate Google Sheets
python populate_spreadsheet.py

# Setup YouTube
python setup_youtube_account.py
```

### Deploy to Cloud

```bash
# On your server
cd ~/youtube-automation
chmod +x deploy.sh
./deploy.sh
```

---

## File Structure

```
youtube-shorts-automation/
├── START_HERE.md              ← You are here
├── README.md                  ← Project overview
├── PUSH_TO_GITHUB.md          ← Push safely
│
├── GitHub Actions (FREE)
│   ├── GITHUB_ACTIONS_GUIDE.md
│   ├── GITHUB_ACTIONS_SETUP.md
│   └── .github/workflows/
│
├── Cloud Hosting
│   ├── HOSTING_GUIDE.md
│   ├── DEPLOYMENT_QUICKSTART.md
│   ├── CHOOSE_DEPLOYMENT.md
│   └── deploy.sh
│
├── Core Code
│   ├── main.py                ← Main pipeline
│   ├── script_generator.py    ← AI scripts
│   ├── voice_generator.py     ← Voice + Whisper
│   ├── image_generator.py     ← AI images
│   ├── video_editor.py        ← Video assembly
│   ├── youtube_uploader.py    ← YouTube API
│   └── automation_scheduler.py
│
├── Automation
│   ├── schedule_3_daily.py    ← Daily scheduler
│   ├── populate_spreadsheet.py ← 500 topics
│   └── google_sheets_integration.py
│
└── Configuration
    ├── .env.example           ← Template
    ├── config.py              ← Settings
    └── requirements.txt       ← Dependencies
```

---

## Common Questions

### Q: Which deployment should I choose?

**A:** Start with GitHub Actions (free). Migrate to cloud server if you need:
- More than 400 videos/month
- Precise scheduling
- Higher reliability

### Q: How much does it cost?

**A:** 
- GitHub Actions: $0 (free tier)
- Cloud Server: $12-30/month
- APIs: $0 (all have free tiers)

### Q: How many videos can I generate?

**A:**
- GitHub Actions: ~400/month (free tier)
- Cloud Server: Unlimited
- Limited by API quotas

### Q: Do I need coding knowledge?

**A:** Basic knowledge helps, but guides are step-by-step. You can copy-paste most commands.

### Q: Can I customize the videos?

**A:** Yes! Edit `config.py` for:
- Video duration
- Voice selection
- Image style
- Subtitle timing

### Q: Is this legal?

**A:** Yes, but:
- Follow YouTube's terms of service
- Don't spam
- Create original content
- Respect API rate limits

---

## Next Steps

### 1. Choose Your Path

- **FREE (Recommended):** Go to `PUSH_TO_GITHUB.md`
- **Cloud Server:** Go to `DEPLOYMENT_QUICKSTART.md`
- **Local Testing:** Run commands above

### 2. Get API Keys

Visit these sites and get free API keys:
- Groq: https://console.groq.com/
- ElevenLabs: https://elevenlabs.io/
- Cloudflare: https://dash.cloudflare.com/
- Google Cloud: https://console.cloud.google.com/

### 3. Follow Setup Guide

- GitHub Actions: `GITHUB_ACTIONS_SETUP.md`
- Cloud Server: `DEPLOYMENT_QUICKSTART.md`

### 4. Generate First Video

Test the system with a simple topic:
```bash
python main.py "benefits of drinking water" --duration 20
```

### 5. Automate

- GitHub Actions: Push to GitHub and add secrets
- Cloud Server: Run `deploy.sh`

---

## Support

### Documentation
- Full guides in repository
- Step-by-step instructions
- Troubleshooting sections

### Logs
- GitHub Actions: Actions tab → Workflow run
- Cloud Server: `tail -f ~/youtube-automation/logs/scheduler.log`

### Common Issues
- Check `GITHUB_ACTIONS_SETUP.md` troubleshooting
- Check `HOSTING_GUIDE.md` troubleshooting
- Review workflow/service logs

---

## Success Checklist

Before going live:

- [ ] All API keys obtained
- [ ] .env file configured (local) OR secrets added (GitHub)
- [ ] Test video generated successfully
- [ ] YouTube authentication working
- [ ] Google Sheets populated with topics
- [ ] Automation tested (manual run)
- [ ] Scheduled automation enabled
- [ ] Monitoring setup

---

## Tips for Success

1. **Start Small:** Test with 5-10 videos first
2. **Monitor Closely:** Check logs daily initially
3. **Optimize Gradually:** Adjust settings based on results
4. **Stay Within Limits:** Respect API quotas
5. **Backup Regularly:** Save your configuration
6. **Update Often:** Keep dependencies updated

---

## Ready to Start?

### For GitHub Actions (FREE):
1. Open `PUSH_TO_GITHUB.md`
2. Follow the checklist
3. Then open `GITHUB_ACTIONS_SETUP.md`

### For Cloud Server:
1. Open `DEPLOYMENT_QUICKSTART.md`
2. Follow the steps
3. Run `deploy.sh`

### For Local Testing:
1. Copy `.env.example` to `.env`
2. Add your API keys
3. Run `python main.py "test topic" --duration 20`

---

**Good luck with your YouTube automation!** 🚀

Questions? Check the documentation files or review the logs.

# YouTube Shorts Automation

Automated YouTube Shorts generation and posting system using AI. Generate engaging health & fitness videos with AI-generated scripts, voiceovers, images, and subtitles.

## Features

- 🤖 AI-powered script generation (Groq/Llama)
- 🎙️ Natural voice synthesis (ElevenLabs)
- 🖼️ AI-generated images (Cloudflare AI)
- 📝 Automatic subtitle synchronization (Whisper AI)
- 📊 Google Sheets integration for topic management
- 📤 Automatic YouTube upload
- ⏰ Scheduled posting (3 videos daily)
- 🔄 Multi-token support for high volume

## Quick Start

### Option 1: GitHub Actions (FREE - Recommended)

Deploy for free using GitHub Actions:

1. **Read the guide:** `GITHUB_ACTIONS_GUIDE.md`
2. **Follow setup:** `GITHUB_ACTIONS_SETUP.md`
3. **Push to GitHub and add secrets**
4. **Videos post automatically!**

**Cost:** $0 (2,000 free minutes/month = ~400 videos)

### Option 2: Cloud Server

Deploy on cloud server for unlimited videos:

1. **Read the guide:** `HOSTING_GUIDE.md`
2. **Quick start:** `DEPLOYMENT_QUICKSTART.md`
3. **Run deployment:** `./deploy.sh`

**Cost:** $12-30/month (unlimited videos)

### Option 3: Local Development

Run locally for testing:

```bash
# Install dependencies
pip install -r requirements.txt
pip install openai-whisper

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Generate a video
python main.py "drinking water benefits" --duration 20

# Populate Google Sheets with topics
python populate_spreadsheet.py

# Setup YouTube authentication
python setup_youtube_account.py
```

## Documentation

### Setup Guides
- **GITHUB_ACTIONS_GUIDE.md** - Complete GitHub Actions guide
- **GITHUB_ACTIONS_SETUP.md** - Step-by-step GitHub Actions setup
- **HOSTING_GUIDE.md** - Cloud server deployment guide
- **DEPLOYMENT_QUICKSTART.md** - Quick cloud deployment
- **CHOOSE_DEPLOYMENT.md** - Compare deployment options

### Configuration
- **.env.example** - Environment variables template
- **config.py** - System configuration
- **requirements.txt** - Python dependencies

## Project Structure

```
├── .github/workflows/       # GitHub Actions workflows
│   ├── daily-videos.yml    # Scheduled automation (3x daily)
│   ├── manual-video.yml    # Manual video generation
│   └── test-setup.yml      # Environment testing
├── utils/                   # Utility modules
├── main.py                  # Main video generation pipeline
├── script_generator.py      # AI script generation
├── voice_generator.py       # Voice synthesis + Whisper
├── image_generator.py       # AI image generation
├── video_editor.py          # Video assembly + subtitles
├── youtube_uploader.py      # YouTube API integration
├── google_sheets_integration.py  # Google Sheets API
├── automation_scheduler.py  # Automation orchestration
├── schedule_3_daily.py      # Daily scheduler (3 videos)
├── populate_spreadsheet.py  # Populate 500 topics
└── setup_youtube_account.py # YouTube authentication
```

## Requirements

### API Keys (Required)

1. **Groq API** - Script generation
   - Get free key: https://console.groq.com/
   
2. **ElevenLabs API** - Voice synthesis
   - Get free key: https://elevenlabs.io/
   - Free tier: 10,000 characters/month
   
3. **Cloudflare AI** - Image generation
   - Get free key: https://dash.cloudflare.com/
   
4. **Google Sheets API** - Topic management
   - Create service account: https://console.cloud.google.com/
   
5. **YouTube Data API** - Video upload
   - Create OAuth2 credentials: https://console.cloud.google.com/

### System Requirements

- Python 3.10+
- FFmpeg
- 4 GB RAM (minimum)
- 10 GB storage

## Configuration

### Environment Variables (.env)

```bash
# AI APIs
GROQ_API_KEY=your_groq_key
ELEVENLABS_API_KEY=your_elevenlabs_key
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_API_TOKEN=your_cloudflare_token

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS=path/to/credentials.json
GOOGLE_SHEETS_ID=your_spreadsheet_id

# YouTube
YOUTUBE_CLIENT_SECRETS=path/to/client_secrets.json

# Optional: Subtitle timing adjustment
SUBTITLE_DELAY=0.3
```

### Video Settings (config.py)

```python
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
VIDEO_FPS = 30
SCRIPT_LENGTH_SECONDS = 20
DEFAULT_VOICE_ID = "TX3LPaxmHKxFdv7VOQHJ"  # Liam (energetic)
```

## Usage

### Generate Single Video

```bash
python main.py "topic name" --duration 20
```

### Populate Google Sheets

```bash
python populate_spreadsheet.py
```

This adds 500+ unique health/fitness topics to your spreadsheet.

### Setup YouTube Authentication

```bash
python setup_youtube_account.py
```

### Run Scheduled Automation

```bash
# Posts 3 videos daily at 9 AM, 3 PM, 9 PM
python schedule_3_daily.py
```

### Manual Automation

```bash
# Process first pending video from Google Sheets
python automation_scheduler.py \
  --sheets-credentials credentials.json \
  --spreadsheet-id YOUR_SHEET_ID \
  --youtube-secrets client_secrets.json \
  --max-videos 1
```

## GitHub Actions Workflows

### Daily Automation (Scheduled)

Runs automatically 3 times per day:
- 9:00 AM UTC
- 3:00 PM UTC
- 9:00 PM UTC

Configure in `.github/workflows/daily-videos.yml`

### Manual Video Generation

Trigger manually from GitHub Actions tab:
1. Go to Actions
2. Select "Generate Single Video (Manual)"
3. Click "Run workflow"
4. Enter topic and duration

### Test Setup

Verify environment and secrets:
1. Go to Actions
2. Select "Test Setup"
3. Click "Run workflow"

## Deployment

### GitHub Actions (Recommended for Beginners)

```bash
# 1. Create GitHub repository
# 2. Push code
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/youtube-automation.git
git push -u origin main

# 3. Add secrets in GitHub Settings
# 4. Enable workflows
# 5. Done!
```

See `GITHUB_ACTIONS_SETUP.md` for detailed instructions.

### Cloud Server (Recommended for Production)

```bash
# 1. Create server (DigitalOcean/AWS/Google Cloud)
# 2. Connect via SSH
ssh ubuntu@YOUR_SERVER_IP

# 3. Upload files
scp -r ./* ubuntu@YOUR_SERVER_IP:~/youtube-automation/

# 4. Run deployment
cd ~/youtube-automation
chmod +x deploy.sh
./deploy.sh
```

See `DEPLOYMENT_QUICKSTART.md` for detailed instructions.

## Troubleshooting

### Video Generation Issues

```bash
# Check FFmpeg
ffmpeg -version

# Test script generation
python -c "from script_generator import generate_script; print(generate_script('test', 20))"

# Test voice generation
python -c "from voice_generator import generate_voice; generate_voice('test', 'output/test.mp3')"
```

### YouTube Authentication

```bash
# Re-authenticate
python setup_youtube_account.py

# This will delete youtube_token.pickle and prompt re-authentication
```

### Google Sheets Connection

```bash
# Test connection
python -c "from google_sheets_integration import GoogleSheetsReader; reader = GoogleSheetsReader(); print('Connected!')"
```

### Subtitle Sync Issues

Adjust `SUBTITLE_DELAY` in `.env`:
- Subtitles too early: Increase value (e.g., 0.5)
- Subtitles too late: Decrease value (e.g., 0.1)

## Cost Breakdown

### GitHub Actions (Free Tier)
- **Cost:** $0/month
- **Limit:** 2,000 minutes/month (~400 videos)
- **Best for:** Testing, low volume

### Cloud Server
- **DigitalOcean:** $12/month (2 GB RAM)
- **AWS EC2:** $15-30/month (t3.medium)
- **Google Cloud:** $20-35/month (e2-medium)
- **Best for:** Production, high volume

### API Costs
- **Groq:** Free (rate limited)
- **ElevenLabs:** Free tier (10k chars/month)
- **Cloudflare AI:** Free tier (10k requests/day)
- **Google Sheets:** Free
- **YouTube API:** Free (10,000 quota/day)

## Features in Detail

### AI Script Generation
- Uses Groq (Llama 3.3 70B)
- Generates engaging 15-30 second scripts
- Optimized for viral content
- Hinglish support

### Voice Synthesis
- ElevenLabs API
- Multiple voice options
- Natural, energetic delivery
- Multi-token support for high volume

### Image Generation
- Cloudflare AI (Stable Diffusion)
- Cinematic 9:16 aspect ratio
- Dramatic lighting
- Scene-specific prompts

### Subtitle Synchronization
- Whisper AI for word-level timing
- 99% accuracy
- Configurable delay compensation
- Smooth animations

### Automation
- Google Sheets for topic management
- Automatic status tracking
- YouTube upload with metadata
- Error handling and retry logic

## Contributing

This is a personal automation project. Feel free to fork and customize for your needs.

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
1. Check documentation files
2. Review workflow logs (GitHub Actions)
3. Check system logs (Cloud server)

## Roadmap

- [ ] Multiple YouTube channel support
- [ ] Advanced analytics integration
- [ ] Custom voice cloning
- [ ] Video templates
- [ ] A/B testing for titles/thumbnails
- [ ] Webhook notifications

## Credits

Built with:
- Groq (Llama 3.3)
- ElevenLabs
- Cloudflare AI
- Whisper AI
- FFmpeg
- Google APIs

---

**Ready to automate your YouTube Shorts?**

Start with GitHub Actions (free): `GITHUB_ACTIONS_SETUP.md`

Or deploy to cloud server: `DEPLOYMENT_QUICKSTART.md`

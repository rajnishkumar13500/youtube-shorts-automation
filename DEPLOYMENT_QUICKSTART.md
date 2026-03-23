# Deployment Quick Start Guide

Fast track guide to deploy your YouTube Shorts automation to the cloud in under 30 minutes.

---

## Prerequisites Checklist

Before deploying, ensure you have:

- [ ] Cloud account (AWS, Google Cloud, or DigitalOcean)
- [ ] `.env` file with all API keys
- [ ] Google Sheets credentials JSON file
- [ ] YouTube OAuth2 client secrets JSON file
- [ ] 500 topics populated in Google Sheets
- [ ] SSH key for server access

---

## Quick Deploy (3 Steps)

### Step 1: Create Server

Choose one platform:

**AWS EC2:**
```
Instance: t3.medium (2 vCPU, 4 GB RAM)
AMI: Ubuntu 22.04 LTS
Storage: 20 GB
Cost: ~$30/month
```

**DigitalOcean (Easiest):**
```
Droplet: Basic (2 GB RAM, 1 vCPU)
Image: Ubuntu 22.04 LTS
Cost: $12/month
```

**Google Cloud:**
```
Machine: e2-medium (2 vCPU, 4 GB RAM)
Image: Ubuntu 22.04 LTS
Cost: ~$35/month
```

### Step 2: Upload Files

From your local machine:

```bash
# Set your server IP
SERVER_IP="YOUR_SERVER_IP"
SERVER_USER="ubuntu"  # or "root" for DigitalOcean

# Upload all project files
scp -r ./* $SERVER_USER@$SERVER_IP:~/youtube-automation/

# Or use rsync (faster for large projects)
rsync -avz --exclude 'output' --exclude '__pycache__' \
  ./ $SERVER_USER@$SERVER_IP:~/youtube-automation/
```

### Step 3: Run Deployment Script

Connect to server and run:

```bash
# Connect to server
ssh $SERVER_USER@$SERVER_IP

# Navigate to project
cd ~/youtube-automation

# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

**Done!** Your automation is now running 24/7.

---

## Manual Setup (If Script Fails)

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv ffmpeg
```

### 2. Setup Project

```bash
mkdir -p ~/youtube-automation
cd ~/youtube-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install openai-whisper
```

### 3. Create Systemd Service

```bash
sudo nano /etc/systemd/system/youtube-automation.service
```

Paste this (adjust paths if using root):

```ini
[Unit]
Description=YouTube Shorts Automation Scheduler
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/youtube-automation
Environment="PATH=/home/ubuntu/youtube-automation/venv/bin"
ExecStart=/home/ubuntu/youtube-automation/venv/bin/python schedule_3_daily.py
Restart=always
RestartSec=10
StandardOutput=append:/home/ubuntu/youtube-automation/logs/scheduler.log
StandardError=append:/home/ubuntu/youtube-automation/logs/scheduler-error.log

[Install]
WantedBy=multi-user.target
```

Save and exit (Ctrl+X, Y, Enter).

### 4. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-automation
sudo systemctl start youtube-automation
sudo systemctl status youtube-automation
```

---

## Essential Commands

### Service Management

```bash
# Check status
sudo systemctl status youtube-automation

# Start service
sudo systemctl start youtube-automation

# Stop service
sudo systemctl stop youtube-automation

# Restart service
sudo systemctl restart youtube-automation

# View logs
sudo journalctl -u youtube-automation -f
```

### Log Monitoring

```bash
# View scheduler logs
tail -f ~/youtube-automation/logs/scheduler.log

# View error logs
tail -f ~/youtube-automation/logs/scheduler-error.log

# View last 50 lines
tail -n 50 ~/youtube-automation/logs/scheduler.log
```

### Testing

```bash
# Test video generation
cd ~/youtube-automation
source venv/bin/activate
python main.py "test topic" --duration 20

# Test Google Sheets connection
python populate_spreadsheet.py

# Test YouTube authentication
python setup_youtube_account.py
```

### System Monitoring

```bash
# Check disk space
df -h

# Check memory
free -h

# Monitor processes
htop

# Check service uptime
sudo systemctl show youtube-automation --property=ActiveEnterTimestamp
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
sudo journalctl -u youtube-automation -n 50

# Test manually
cd ~/youtube-automation
source venv/bin/activate
python schedule_3_daily.py
```

### Out of Memory

```bash
# Add 2GB swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### YouTube Authentication

```bash
# Re-authenticate
cd ~/youtube-automation
source venv/bin/activate
python setup_youtube_account.py
```

### Wrong Timezone

```bash
# Check timezone
timedatectl

# Set timezone (example: India)
sudo timedatectl set-timezone Asia/Kolkata

# Restart service
sudo systemctl restart youtube-automation
```

---

## File Upload Commands

### Upload Single File

```bash
scp .env ubuntu@YOUR_SERVER_IP:~/youtube-automation/
```

### Upload Multiple Files

```bash
scp *.json ubuntu@YOUR_SERVER_IP:~/youtube-automation/
scp *.py ubuntu@YOUR_SERVER_IP:~/youtube-automation/
```

### Upload Entire Directory

```bash
rsync -avz --exclude 'output' --exclude '__pycache__' \
  ./ ubuntu@YOUR_SERVER_IP:~/youtube-automation/
```

### Download Logs

```bash
scp ubuntu@YOUR_SERVER_IP:~/youtube-automation/logs/*.log ./logs/
```

---

## Security Checklist

- [ ] Change default SSH port (optional)
- [ ] Disable password authentication
- [ ] Enable firewall (UFW)
- [ ] Set proper file permissions (600 for .env and .json)
- [ ] Regular system updates
- [ ] Monitor logs for suspicious activity

---

## Cost Optimization

### Reduce Costs

1. **Use smaller instance during testing**
   - Start with 2GB RAM
   - Upgrade if needed

2. **Use spot instances (AWS)**
   - Save up to 70%
   - Good for non-critical workloads

3. **Schedule instance stop/start**
   - Stop during low-activity hours
   - Use AWS Lambda or cron jobs

4. **Monitor bandwidth usage**
   - Optimize video file sizes
   - Use compression

---

## Monitoring Setup

### Create Monitoring Script

```bash
nano ~/monitor.sh
```

Add:

```bash
#!/bin/bash
echo "=== System Status ==="
date
echo ""
echo "Service Status:"
sudo systemctl status youtube-automation --no-pager | head -n 5
echo ""
echo "Disk Usage:"
df -h | grep -E "/$|/home"
echo ""
echo "Memory Usage:"
free -h
echo ""
echo "Last 5 Log Entries:"
tail -n 5 ~/youtube-automation/logs/scheduler.log
```

Make executable:

```bash
chmod +x ~/monitor.sh
```

Run:

```bash
./monitor.sh
```

### Setup Cron for Daily Reports

```bash
crontab -e
```

Add:

```bash
# Daily status report at 11 PM
0 23 * * * ~/monitor.sh >> ~/daily-report.log 2>&1
```

---

## Backup Strategy

### Backup Important Files

```bash
# Create backup script
nano ~/backup.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR=~/backups
DATE=$(date +%Y%m%d)
mkdir -p $BACKUP_DIR

# Backup configuration
tar -czf $BACKUP_DIR/config-$DATE.tar.gz \
  ~/youtube-automation/.env \
  ~/youtube-automation/*.json \
  ~/youtube-automation/*.pickle

# Backup logs
tar -czf $BACKUP_DIR/logs-$DATE.tar.gz \
  ~/youtube-automation/logs/

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable and run:

```bash
chmod +x ~/backup.sh
./backup.sh
```

### Schedule Daily Backups

```bash
crontab -e
```

Add:

```bash
# Daily backup at 2 AM
0 2 * * * ~/backup.sh >> ~/backup.log 2>&1
```

---

## Performance Tuning

### Optimize FFmpeg

Edit `config.py`:

```python
# Use faster encoding preset
VIDEO_ENCODING_PRESET = "ultrafast"  # or "veryfast"

# Reduce video quality slightly
VIDEO_CRF = 28  # Higher = smaller file, lower quality (default: 23)
```

### Reduce Memory Usage

```python
# In config.py
IMAGE_QUALITY = 85  # Reduce from 95
VIDEO_BITRATE = "2M"  # Reduce from "4M"
```

### Parallel Processing

For multiple videos:

```python
# In schedule_3_daily.py
# Add delay between videos
time.sleep(30)  # 30 seconds between uploads
```

---

## Success Checklist

After deployment, verify:

- [ ] Service is running: `sudo systemctl status youtube-automation`
- [ ] Logs are being written: `tail -f ~/youtube-automation/logs/scheduler.log`
- [ ] No errors in error log: `tail ~/youtube-automation/logs/scheduler-error.log`
- [ ] Disk space available: `df -h`
- [ ] Memory sufficient: `free -h`
- [ ] Timezone correct: `timedatectl`
- [ ] Google Sheets accessible
- [ ] YouTube authentication working
- [ ] First video posted successfully

---

## Support Resources

### Documentation

- Full hosting guide: `HOSTING_GUIDE.md`
- Setup guide: `QUICK_SETUP.md`
- YouTube setup: `YOUTUBE_SETUP_GUIDE.md`

### Logs Location

- Scheduler logs: `~/youtube-automation/logs/scheduler.log`
- Error logs: `~/youtube-automation/logs/scheduler-error.log`
- Systemd logs: `sudo journalctl -u youtube-automation`

### Common Issues

1. **Service fails to start**: Check logs and file permissions
2. **Out of memory**: Add swap space or upgrade instance
3. **YouTube auth fails**: Re-run `setup_youtube_account.py`
4. **Videos not posting**: Check timezone and scheduler logs

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────┐
│         YouTube Automation Quick Commands           │
├─────────────────────────────────────────────────────┤
│ Start:    sudo systemctl start youtube-automation  │
│ Stop:     sudo systemctl stop youtube-automation   │
│ Restart:  sudo systemctl restart youtube-automation│
│ Status:   sudo systemctl status youtube-automation │
│ Logs:     tail -f ~/youtube-automation/logs/*.log  │
│ Monitor:  htop                                      │
│ Disk:     df -h                                     │
│ Memory:   free -h                                   │
└─────────────────────────────────────────────────────┘
```

---

**Your automation is now live!** 🎉

Videos will post automatically at 9 AM, 3 PM, and 9 PM daily.

Check your YouTube channel: https://youtube.com/
Check your Google Sheets for status updates.

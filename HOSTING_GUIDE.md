# Cloud Hosting Guide for YouTube Shorts Automation

Complete guide to deploy your YouTube Shorts automation system on cloud platforms for 24/7 operation.

---

## Table of Contents

1. [Overview](#overview)
2. [Cloud Platform Options](#cloud-platform-options)
3. [Prerequisites](#prerequisites)
4. [Option 1: AWS EC2 (Recommended)](#option-1-aws-ec2-recommended)
5. [Option 2: Google Cloud Compute Engine](#option-2-google-cloud-compute-engine)
6. [Option 3: DigitalOcean Droplet](#option-3-digitalocean-droplet)
7. [Server Setup (All Platforms)](#server-setup-all-platforms)
8. [Systemd Service Configuration](#systemd-service-configuration)
9. [Monitoring & Logging](#monitoring--logging)
10. [Cost Estimates](#cost-estimates)
11. [Troubleshooting](#troubleshooting)

---

## Overview

Your automation system will:
- Run 24/7 on a cloud server
- Post 3 videos daily at 9 AM, 3 PM, and 9 PM
- Process 500 topics from Google Sheets
- Automatically restart if it crashes
- Log all activities for monitoring

**System Requirements:**
- 2 CPU cores minimum
- 4 GB RAM minimum (8 GB recommended)
- 20 GB storage minimum
- Ubuntu 22.04 LTS (recommended)
- Python 3.10+
- FFmpeg for video processing

---

## Cloud Platform Options

### Comparison Table

| Platform | Monthly Cost | Setup Difficulty | Best For |
|----------|-------------|------------------|----------|
| AWS EC2 | $15-30 | Medium | Scalability, reliability |
| Google Cloud | $20-35 | Medium | Google integration |
| DigitalOcean | $12-24 | Easy | Simplicity, beginners |

---

## Prerequisites

Before starting, ensure you have:

1. ✅ All API keys configured in `.env` file
2. ✅ Google Sheets populated with 500 topics
3. ✅ YouTube authentication working locally
4. ✅ All Python dependencies listed in `requirements.txt`
5. ✅ Service account JSON files for Google Sheets
6. ✅ OAuth2 client secrets for YouTube

---

## Option 1: AWS EC2 (Recommended)

### Step 1: Create EC2 Instance

1. **Login to AWS Console**
   - Go to https://console.aws.amazon.com/
   - Navigate to EC2 Dashboard

2. **Launch Instance**
   ```
   Name: youtube-shorts-automation
   AMI: Ubuntu Server 22.04 LTS
   Instance Type: t3.medium (2 vCPU, 4 GB RAM)
   Key Pair: Create new or use existing
   Storage: 20 GB gp3
   ```

3. **Configure Security Group**
   - Allow SSH (port 22) from your IP
   - No other ports needed (outbound only)

4. **Launch Instance**
   - Wait for instance to start
   - Note the public IP address

### Step 2: Connect to Instance

```bash
# Download your key pair (e.g., youtube-automation.pem)
chmod 400 youtube-automation.pem

# Connect via SSH
ssh -i youtube-automation.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3: Setup Server

Continue to [Server Setup](#server-setup-all-platforms) section.

---

## Option 2: Google Cloud Compute Engine

### Step 1: Create VM Instance

1. **Login to Google Cloud Console**
   - Go to https://console.cloud.google.com/
   - Navigate to Compute Engine > VM Instances

2. **Create Instance**
   ```
   Name: youtube-shorts-automation
   Region: us-central1 (or nearest)
   Machine Type: e2-medium (2 vCPU, 4 GB RAM)
   Boot Disk: Ubuntu 22.04 LTS, 20 GB
   Firewall: Allow HTTP/HTTPS (optional)
   ```

3. **Create Instance**
   - Click "Create"
   - Wait for VM to start

### Step 2: Connect to Instance

```bash
# Use gcloud CLI (install from https://cloud.google.com/sdk/docs/install)
gcloud compute ssh youtube-shorts-automation --zone=us-central1-a

# Or use SSH from browser (click "SSH" button in console)
```

### Step 3: Setup Server

Continue to [Server Setup](#server-setup-all-platforms) section.

---

## Option 3: DigitalOcean Droplet

### Step 1: Create Droplet

1. **Login to DigitalOcean**
   - Go to https://cloud.digitalocean.com/
   - Click "Create" > "Droplets"

2. **Configure Droplet**
   ```
   Image: Ubuntu 22.04 LTS
   Plan: Basic
   CPU: Regular (2 GB RAM / 1 vCPU) or $12/month
        OR Premium (4 GB RAM / 2 vCPU) for $24/month
   Datacenter: Nearest to you
   Authentication: SSH Key (recommended) or Password
   Hostname: youtube-shorts-automation
   ```

3. **Create Droplet**
   - Click "Create Droplet"
   - Wait for droplet to start
   - Note the IP address

### Step 2: Connect to Droplet

```bash
# Connect via SSH
ssh root@YOUR_DROPLET_IP

# Or if using SSH key
ssh -i ~/.ssh/your_key root@YOUR_DROPLET_IP
```

### Step 3: Setup Server

Continue to [Server Setup](#server-setup-all-platforms) section.

---

## Server Setup (All Platforms)

Once connected to your server, follow these steps:

### Step 1: Update System

```bash
# Update package list
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Install essential tools
sudo apt install -y git python3 python3-pip python3-venv ffmpeg
```

### Step 2: Install Python Dependencies

```bash
# Check Python version (should be 3.10+)
python3 --version

# Install pip
sudo apt install -y python3-pip

# Upgrade pip
python3 -m pip install --upgrade pip
```

### Step 3: Clone Your Project

```bash
# Create project directory
mkdir -p ~/youtube-automation
cd ~/youtube-automation

# Option A: Upload files via SCP (from your local machine)
# scp -r /path/to/your/project/* ubuntu@YOUR_SERVER_IP:~/youtube-automation/

# Option B: Clone from Git (if you have a repository)
# git clone https://github.com/yourusername/youtube-automation.git .

# Option C: Use rsync (recommended for large projects)
# rsync -avz -e "ssh -i your-key.pem" /path/to/project/ ubuntu@YOUR_SERVER_IP:~/youtube-automation/
```

### Step 4: Upload Required Files

From your local machine, upload these critical files:

```bash
# Upload .env file
scp -i your-key.pem .env ubuntu@YOUR_SERVER_IP:~/youtube-automation/

# Upload Google Sheets credentials
scp -i your-key.pem youtube-automation-*.json ubuntu@YOUR_SERVER_IP:~/youtube-automation/

# Upload YouTube client secrets
scp -i your-key.pem client_secret_*.json ubuntu@YOUR_SERVER_IP:~/youtube-automation/

# Upload YouTube token (if you have it)
scp -i your-key.pem youtube_token.pickle ubuntu@YOUR_SERVER_IP:~/youtube-automation/
```

### Step 5: Create Virtual Environment

```bash
cd ~/youtube-automation

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 6: Install Whisper (for subtitle sync)

```bash
# Install Whisper AI
pip install openai-whisper

# Install ffmpeg (if not already installed)
sudo apt install -y ffmpeg
```

### Step 7: Test the System

```bash
# Activate virtual environment
source venv/bin/activate

# Test video generation
python main.py "test topic" --duration 20

# If successful, you should see output/final_video_final.mp4
```

---

## Systemd Service Configuration

Create a systemd service to run your scheduler 24/7 with auto-restart.

### Step 1: Create Service File

```bash
sudo nano /etc/systemd/system/youtube-automation.service
```

### Step 2: Add Service Configuration

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

**Note:** If using `root` user (DigitalOcean), change:
- `User=ubuntu` to `User=root`
- `/home/ubuntu/` to `/root/`

### Step 3: Create Logs Directory

```bash
mkdir -p ~/youtube-automation/logs
```

### Step 4: Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable youtube-automation

# Start service
sudo systemctl start youtube-automation

# Check status
sudo systemctl status youtube-automation
```

### Step 5: Manage Service

```bash
# Stop service
sudo systemctl stop youtube-automation

# Restart service
sudo systemctl restart youtube-automation

# View logs
sudo journalctl -u youtube-automation -f

# View last 100 lines
sudo journalctl -u youtube-automation -n 100
```

---

## Monitoring & Logging

### View Real-Time Logs

```bash
# View scheduler logs
tail -f ~/youtube-automation/logs/scheduler.log

# View error logs
tail -f ~/youtube-automation/logs/scheduler-error.log

# View systemd logs
sudo journalctl -u youtube-automation -f
```

### Check Service Status

```bash
# Check if service is running
sudo systemctl status youtube-automation

# Check if service is enabled
sudo systemctl is-enabled youtube-automation

# Check service uptime
sudo systemctl show youtube-automation --property=ActiveEnterTimestamp
```

### Monitor System Resources

```bash
# Install htop
sudo apt install -y htop

# Monitor CPU/RAM usage
htop

# Check disk space
df -h

# Check memory usage
free -h
```

### Setup Log Rotation

Prevent logs from filling up disk space:

```bash
# Create logrotate config
sudo nano /etc/logrotate.d/youtube-automation
```

Add this configuration:

```
/home/ubuntu/youtube-automation/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 ubuntu ubuntu
}
```

---

## Cost Estimates

### AWS EC2

| Instance Type | vCPU | RAM | Storage | Monthly Cost |
|--------------|------|-----|---------|--------------|
| t3.small | 2 | 2 GB | 20 GB | ~$15 |
| t3.medium | 2 | 4 GB | 20 GB | ~$30 |
| t3.large | 2 | 8 GB | 20 GB | ~$60 |

**Additional Costs:**
- Data transfer: ~$0.09/GB (first 100 GB free)
- Storage: ~$0.10/GB/month

**Estimated Total:** $15-30/month

### Google Cloud Compute Engine

| Machine Type | vCPU | RAM | Storage | Monthly Cost |
|-------------|------|-----|---------|--------------|
| e2-small | 2 | 2 GB | 20 GB | ~$20 |
| e2-medium | 2 | 4 GB | 20 GB | ~$35 |
| e2-standard-2 | 2 | 8 GB | 20 GB | ~$50 |

**Additional Costs:**
- Network egress: ~$0.12/GB
- Storage: ~$0.04/GB/month

**Estimated Total:** $20-35/month

### DigitalOcean

| Droplet Size | vCPU | RAM | Storage | Monthly Cost |
|-------------|------|-----|---------|--------------|
| Basic | 1 | 2 GB | 50 GB | $12 |
| Basic | 2 | 4 GB | 80 GB | $24 |
| Premium | 2 | 8 GB | 160 GB | $48 |

**Additional Costs:**
- Bandwidth: 2-4 TB included
- Backups: +20% of droplet cost (optional)

**Estimated Total:** $12-24/month

---

## Troubleshooting

### Service Won't Start

```bash
# Check service status
sudo systemctl status youtube-automation

# View detailed logs
sudo journalctl -u youtube-automation -n 50

# Check if Python path is correct
which python3

# Test script manually
cd ~/youtube-automation
source venv/bin/activate
python schedule_3_daily.py
```

### Video Generation Fails

```bash
# Check FFmpeg installation
ffmpeg -version

# Check disk space
df -h

# Check memory
free -h

# View error logs
tail -f ~/youtube-automation/logs/scheduler-error.log
```

### YouTube Authentication Issues

```bash
# Re-authenticate YouTube
cd ~/youtube-automation
source venv/bin/activate
python setup_youtube_account.py

# This will delete youtube_token.pickle and prompt re-authentication
```

### Google Sheets Connection Issues

```bash
# Verify credentials file exists
ls -la ~/youtube-automation/*.json

# Check .env file
cat ~/youtube-automation/.env | grep GOOGLE_SHEETS

# Test connection
python -c "from google_sheets_integration import GoogleSheetsReader; reader = GoogleSheetsReader(); print('Connected!')"
```

### Out of Memory Errors

```bash
# Check memory usage
free -h

# Add swap space (if needed)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make swap permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Scheduler Not Running at Scheduled Times

```bash
# Check system time
date

# Check timezone
timedatectl

# Set timezone (if needed)
sudo timedatectl set-timezone Asia/Kolkata

# Restart service
sudo systemctl restart youtube-automation
```

---

## Security Best Practices

### 1. Secure SSH Access

```bash
# Disable password authentication
sudo nano /etc/ssh/sshd_config

# Set: PasswordAuthentication no
# Restart SSH
sudo systemctl restart sshd
```

### 2. Setup Firewall

```bash
# Install UFW
sudo apt install -y ufw

# Allow SSH
sudo ufw allow 22/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 3. Protect Sensitive Files

```bash
# Set proper permissions
chmod 600 ~/youtube-automation/.env
chmod 600 ~/youtube-automation/*.json
chmod 600 ~/youtube-automation/youtube_token.pickle
```

### 4. Regular Updates

```bash
# Create update script
nano ~/update.sh
```

Add:

```bash
#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo systemctl restart youtube-automation
```

Make executable:

```bash
chmod +x ~/update.sh
```

---

## Quick Start Commands

### Deploy to Server

```bash
# 1. Connect to server
ssh -i your-key.pem ubuntu@YOUR_SERVER_IP

# 2. Setup system
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip python3-venv ffmpeg

# 3. Create project directory
mkdir -p ~/youtube-automation
cd ~/youtube-automation

# 4. Upload files (from local machine)
scp -r /path/to/project/* ubuntu@YOUR_SERVER_IP:~/youtube-automation/

# 5. Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install openai-whisper

# 6. Create systemd service
sudo nano /etc/systemd/system/youtube-automation.service
# (paste service configuration from above)

# 7. Start service
sudo systemctl daemon-reload
sudo systemctl enable youtube-automation
sudo systemctl start youtube-automation

# 8. Check status
sudo systemctl status youtube-automation
```

---

## Next Steps

1. ✅ Choose a cloud platform (AWS, Google Cloud, or DigitalOcean)
2. ✅ Create server instance
3. ✅ Upload your project files
4. ✅ Setup systemd service
5. ✅ Monitor logs and ensure videos are posting
6. ✅ Setup log rotation
7. ✅ Configure backups (optional)

---

## Support

If you encounter issues:

1. Check logs: `tail -f ~/youtube-automation/logs/scheduler.log`
2. Check service status: `sudo systemctl status youtube-automation`
3. Test manually: `python schedule_3_daily.py`
4. Review error logs: `sudo journalctl -u youtube-automation -n 100`

---

**Your automation is now running 24/7 in the cloud!** 🚀

Videos will be posted automatically at:
- 9:00 AM
- 3:00 PM  
- 9:00 PM

Check your YouTube channel and Google Sheets to monitor progress.

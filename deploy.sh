#!/bin/bash

# YouTube Shorts Automation - Cloud Deployment Script
# This script automates the server setup process

set -e  # Exit on error

echo "=========================================="
echo "YouTube Shorts Automation - Deployment"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    USER_HOME="/root"
    SERVICE_USER="root"
else
    USER_HOME="$HOME"
    SERVICE_USER="$USER"
fi

PROJECT_DIR="$USER_HOME/youtube-automation"

echo -e "${GREEN}✓${NC} Running as user: $SERVICE_USER"
echo -e "${GREEN}✓${NC} Project directory: $PROJECT_DIR"
echo ""

# Step 1: Update system
echo "=========================================="
echo "Step 1: Updating system packages"
echo "=========================================="
sudo apt update
sudo apt upgrade -y
echo -e "${GREEN}✓${NC} System updated"
echo ""

# Step 2: Install dependencies
echo "=========================================="
echo "Step 2: Installing dependencies"
echo "=========================================="
sudo apt install -y git python3 python3-pip python3-venv ffmpeg htop
echo -e "${GREEN}✓${NC} Dependencies installed"
echo ""

# Step 3: Create project directory
echo "=========================================="
echo "Step 3: Setting up project directory"
echo "=========================================="
mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/output"
mkdir -p "$PROJECT_DIR/output/audio"
mkdir -p "$PROJECT_DIR/output/images"
cd "$PROJECT_DIR"
echo -e "${GREEN}✓${NC} Project directory created"
echo ""

# Step 4: Setup Python virtual environment
echo "=========================================="
echo "Step 4: Setting up Python environment"
echo "=========================================="
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
echo -e "${GREEN}✓${NC} Virtual environment created"
echo ""

# Step 5: Install Python packages
echo "=========================================="
echo "Step 5: Installing Python packages"
echo "=========================================="
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo -e "${GREEN}✓${NC} Requirements installed"
else
    echo -e "${YELLOW}⚠${NC} requirements.txt not found, installing common packages..."
    pip install groq elevenlabs requests python-dotenv google-api-python-client google-auth-httplib2 google-auth-oauthlib openai-whisper
fi

# Install Whisper
pip install openai-whisper
echo -e "${GREEN}✓${NC} Whisper AI installed"
echo ""

# Step 6: Create systemd service
echo "=========================================="
echo "Step 6: Creating systemd service"
echo "=========================================="

SERVICE_FILE="/etc/systemd/system/youtube-automation.service"

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=YouTube Shorts Automation Scheduler
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/python schedule_3_daily.py
Restart=always
RestartSec=10
StandardOutput=append:$PROJECT_DIR/logs/scheduler.log
StandardError=append:$PROJECT_DIR/logs/scheduler-error.log

[Install]
WantedBy=multi-user.target
EOF

echo -e "${GREEN}✓${NC} Systemd service created"
echo ""

# Step 7: Setup log rotation
echo "=========================================="
echo "Step 7: Setting up log rotation"
echo "=========================================="

LOGROTATE_FILE="/etc/logrotate.d/youtube-automation"

sudo tee "$LOGROTATE_FILE" > /dev/null <<EOF
$PROJECT_DIR/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $SERVICE_USER $SERVICE_USER
}
EOF

echo -e "${GREEN}✓${NC} Log rotation configured"
echo ""

# Step 8: Setup firewall (optional)
echo "=========================================="
echo "Step 8: Configuring firewall"
echo "=========================================="
if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp
    echo -e "${GREEN}✓${NC} Firewall configured (SSH allowed)"
else
    echo -e "${YELLOW}⚠${NC} UFW not installed, skipping firewall setup"
fi
echo ""

# Step 9: Set file permissions
echo "=========================================="
echo "Step 9: Setting file permissions"
echo "=========================================="
if [ -f "$PROJECT_DIR/.env" ]; then
    chmod 600 "$PROJECT_DIR/.env"
    echo -e "${GREEN}✓${NC} .env permissions set"
fi

if ls "$PROJECT_DIR"/*.json 1> /dev/null 2>&1; then
    chmod 600 "$PROJECT_DIR"/*.json
    echo -e "${GREEN}✓${NC} JSON credentials permissions set"
fi

if [ -f "$PROJECT_DIR/youtube_token.pickle" ]; then
    chmod 600 "$PROJECT_DIR/youtube_token.pickle"
    echo -e "${GREEN}✓${NC} YouTube token permissions set"
fi
echo ""

# Step 10: Enable and start service
echo "=========================================="
echo "Step 10: Starting automation service"
echo "=========================================="
sudo systemctl daemon-reload
sudo systemctl enable youtube-automation
echo -e "${GREEN}✓${NC} Service enabled (will start on boot)"
echo ""

# Check if all required files exist before starting
MISSING_FILES=0

if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo -e "${RED}✗${NC} Missing: .env file"
    MISSING_FILES=1
fi

if [ ! -f "$PROJECT_DIR/schedule_3_daily.py" ]; then
    echo -e "${RED}✗${NC} Missing: schedule_3_daily.py"
    MISSING_FILES=1
fi

if ! ls "$PROJECT_DIR"/*.json 1> /dev/null 2>&1; then
    echo -e "${YELLOW}⚠${NC} Warning: No JSON credential files found"
fi

if [ $MISSING_FILES -eq 1 ]; then
    echo ""
    echo -e "${YELLOW}⚠${NC} Some required files are missing."
    echo "Please upload them before starting the service:"
    echo ""
    echo "  scp .env $SERVICE_USER@YOUR_SERVER_IP:$PROJECT_DIR/"
    echo "  scp *.json $SERVICE_USER@YOUR_SERVER_IP:$PROJECT_DIR/"
    echo "  scp *.py $SERVICE_USER@YOUR_SERVER_IP:$PROJECT_DIR/"
    echo ""
    echo "Then run: sudo systemctl start youtube-automation"
else
    sudo systemctl start youtube-automation
    echo -e "${GREEN}✓${NC} Service started"
fi
echo ""

# Step 11: Display status
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Service Status:"
sudo systemctl status youtube-automation --no-pager || true
echo ""
echo "=========================================="
echo "Useful Commands:"
echo "=========================================="
echo ""
echo "View logs:"
echo "  tail -f $PROJECT_DIR/logs/scheduler.log"
echo ""
echo "Check service status:"
echo "  sudo systemctl status youtube-automation"
echo ""
echo "Restart service:"
echo "  sudo systemctl restart youtube-automation"
echo ""
echo "Stop service:"
echo "  sudo systemctl stop youtube-automation"
echo ""
echo "View systemd logs:"
echo "  sudo journalctl -u youtube-automation -f"
echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Verify all files are uploaded:"
echo "   ls -la $PROJECT_DIR"
echo ""
echo "2. Check .env configuration:"
echo "   cat $PROJECT_DIR/.env"
echo ""
echo "3. Test video generation:"
echo "   cd $PROJECT_DIR"
echo "   source venv/bin/activate"
echo "   python main.py 'test topic' --duration 20"
echo ""
echo "4. Monitor logs:"
echo "   tail -f $PROJECT_DIR/logs/scheduler.log"
echo ""
echo "=========================================="
echo "Videos will be posted at:"
echo "  - 9:00 AM"
echo "  - 3:00 PM"
echo "  - 9:00 PM"
echo "=========================================="
echo ""

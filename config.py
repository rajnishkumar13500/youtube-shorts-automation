"""
Configuration for YouTube Shorts Automation.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# API Keys (from environment variables)
# ============================================================================

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# Cloudflare AI credentials for image generation
CLOUDFLARE_ACCOUNT_ID: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_API_TOKEN: str = os.getenv("CLOUDFLARE_API_TOKEN", "")


# ============================================================================
# Video Settings
# ============================================================================

VIDEO_WIDTH: int = 1080
VIDEO_HEIGHT: int = 1920
IMAGE_DURATION: float = 1.2  # seconds per image
VIDEO_FPS: int = 30


# ============================================================================
# Output Directory Structure
# ============================================================================

OUTPUT_DIR: str = "output"
AUDIO_DIR: str = os.path.join(OUTPUT_DIR, "audio")
IMAGES_DIR: str = os.path.join(OUTPUT_DIR, "images")
LOGS_DIR: str = os.path.join(OUTPUT_DIR, "logs")

# Ensure output directories exist
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
Path(AUDIO_DIR).mkdir(parents=True, exist_ok=True)
Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)
Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)


# ============================================================================
# File Paths
# ============================================================================

AUDIO_OUTPUT_PATH: str = os.path.join(AUDIO_DIR, "audio.mp3")
FINAL_VIDEO_PATH: str = os.path.join(OUTPUT_DIR, "final_video.mp4")


# ============================================================================
# Script Generation Settings
# ============================================================================

SCRIPT_LENGTH_SECONDS: int = 15
SCRIPT_LANGUAGE: str = "Hinglish"  # Hindi + English mix
SCRIPT_FORMAT: str = "dramatic, with emotional markers like [slow], [pause], [intense]"

# Groq Model Options:
# - llama-3.3-70b-versatile (RECOMMENDED - fast, reliable, high quality)
# - mixtral-8x7b-32768 (good for creative content)
# - llama3-70b-8192 (alternative Llama model)
# - gemma2-9b-it (faster, smaller model)
# - openai/gpt-oss-120b (GPT OSS model - sometimes unreliable)
DEFAULT_GROQ_MODEL: str = "llama-3.3-70b-versatile"  # Llama 3.3 - reliable and fast


# ============================================================================
# Voice Generation Settings
# ============================================================================

# Free tier voice IDs (premade voices - no payment required):
# - TX3LPaxmHKxFdv7VOQHJ: Liam - Energetic, Social Media Creator (RECOMMENDED for Shorts)
# - IKne3meq5aSn9XLyUdCD: Charlie - Deep, Confident, Energetic
# - Xb7hH8MSUJpSbSDYk0k2: Alice - Clear, Engaging Educator
# - JBFqnCBsd6RMkjVDRZzb: George - Warm, Captivating Storyteller
#
# Professional voices (require paid plan):
# - yRis6UiS4dtT4Aqv72DC: Ranbir - Deep, Magnetic (Hindi)

DEFAULT_VOICE_ID: str = "TX3LPaxmHKxFdv7VOQHJ"  # Liam - Energetic (FREE, great for shorts!)
VOICE_STABILITY: float = 0.75
VOICE_SIMILARITY_BOOST: float = 0.75


# ============================================================================
# Image Generation Settings
# ============================================================================

IMAGE_WIDTH: int = 1080
IMAGE_HEIGHT: int = 1920
IMAGE_ASPECT_RATIO: str = "9:16"
IMAGE_STYLE: str = "cinematic, 3D, dramatic lighting"


# ============================================================================
# Viral Content Settings
# ============================================================================

# Sound effects for viral content (optional - can be added in post-production)
SOUND_EFFECTS_ENABLED: bool = os.getenv("SOUND_EFFECTS_ENABLED", "false").lower() == "true"

# Hook styles for viral content
HOOK_STYLES = [
    "Kya aap jaante hain...",  # Do you know...
    "Yeh sunke aap shocked ho jayenge!",  # You'll be shocked hearing this!
    "Doctors yeh baat chhupate hain!",  # Doctors hide this fact!
    "Yeh secret koi nahi batata!",  # Nobody tells this secret!
    "Aapko pata hai kya hoga agar...",  # Do you know what will happen if...
]

# Viral content optimization
VIRAL_OPTIMIZATION: bool = True  # Enable viral-optimized scripts
MIN_HOOK_DURATION: float = 3.0  # Minimum 3 seconds for hook
SUSPENSE_PAUSES: bool = True  # Add strategic pauses for suspense


# ============================================================================
# Subtitle Synchronization Settings
# ============================================================================

# Subtitle delay to compensate for Whisper timing being too fast
# Whisper often gives timestamps that are ahead of actual speech
# Adjust this value if subtitles appear too early or too late
# Positive values delay subtitles, negative values make them appear earlier
SUBTITLE_DELAY: float = float(os.getenv("SUBTITLE_DELAY", "0.3"))  # Default: 300ms delay


# ============================================================================
# Background Music Settings
# ============================================================================

# Path to default background music file (optional)
DEFAULT_BG_MUSIC_PATH: str = os.getenv("DEFAULT_BG_MUSIC_PATH", "")

# Background music volume relative to voice audio (0.0 to 1.0)
# Lower values mean background music is quieter
BG_MUSIC_VOLUME: float = 0.3  # Background music at 30% of voice volume

# Enable/disable background music by default
ENABLE_BG_MUSIC: bool = os.getenv("ENABLE_BG_MUSIC", "false").lower() == "true"

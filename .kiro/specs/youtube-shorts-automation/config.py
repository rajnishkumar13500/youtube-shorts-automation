"""
Configuration module for YouTube Shorts Automation.
Loads environment variables and provides configuration values.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


def _get_required_env_var(name: str) -> str:
    """
    Get a required environment variable with helpful error message.
    
    Args:
        name: Environment variable name
        
    Returns:
        Environment variable value
        
    Raises:
        ConfigError: If environment variable is not set
    """
    value = os.getenv(name)
    if not value:
        raise ConfigError(
            f"Missing required environment variable: {name}\n"
            f"Please set it in your .env file or environment.\n"
            f"Visit the service documentation to get your API key."
        )
    return value


# API Keys - validated at import time
OPENAI_API_KEY = _get_required_env_var("OPENAI_API_KEY")
ELEVENLABS_API_KEY = _get_required_env_var("ELEVENLABS_API_KEY")
STABILITY_API_KEY = _get_required_env_var("STABILITY_API_KEY")

# Video Settings
VIDEO_WIDTH = int(os.getenv("VIDEO_WIDTH", "1080"))
VIDEO_HEIGHT = int(os.getenv("VIDEO_HEIGHT", "1920"))
IMAGE_DURATION = float(os.getenv("IMAGE_DURATION", "1.2"))

# Output Directory Structure
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "images"
AUDIO_DIR = OUTPUT_DIR / "audio"
FINAL_VIDEO_PATH = OUTPUT_DIR / "final_video.mp4"
AUDIO_PATH = AUDIO_DIR / "audio.mp3"

# Create output directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def validate_config() -> bool:
    """
    Validate all configuration values.
    
    Returns:
        True if configuration is valid
        
    Raises:
        ConfigError: If any configuration value is invalid
    """
    errors = []
    
    # Validate API keys are not empty strings
    if not OPENAI_API_KEY.strip():
        errors.append("OPENAI_API_KEY cannot be empty")
    if not ELEVENLABS_API_KEY.strip():
        errors.append("ELEVENLABS_API_KEY cannot be empty")
    if not STABILITY_API_KEY.strip():
        errors.append("STABILITY_API_KEY cannot be empty")
    
    # Validate video settings
    if VIDEO_WIDTH <= 0:
        errors.append("VIDEO_WIDTH must be positive")
    if VIDEO_HEIGHT <= 0:
        errors.append("VIDEO_HEIGHT must be positive")
    if IMAGE_DURATION <= 0:
        errors.append("IMAGE_DURATION must be positive")
    
    if errors:
        raise ConfigError("Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors))
    
    return True


# Validate configuration on import
validate_config()


# Output path helper functions
def get_audio_path(filename: str = "audio.mp3") -> Path:
    """
    Get the full path for an audio file.
    
    Args:
        filename: Audio filename (default: "audio.mp3")
        
    Returns:
        Full path to audio file
    """
    return OUTPUT_DIR / filename


def get_image_path(scene_number: int) -> Path:
    """
    Get the full path for a scene image.
    
    Args:
        scene_number: Scene number (1-indexed)
        
    Returns:
        Full path to scene image
    """
    return IMAGES_DIR / f"scene_{scene_number}.png"


def get_video_path(filename: str = "final_video.mp4") -> Path:
    """
    Get the full path for a video file.
    
    Args:
        filename: Video filename (default: "final_video.mp4")
        
    Returns:
        Full path to video file
    """
    return OUTPUT_DIR / filename


def ensure_output_directories() -> None:
    """
    Ensure all output directories exist. Creates them if they don't exist.
    This function can be called to recreate directories if they were deleted.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

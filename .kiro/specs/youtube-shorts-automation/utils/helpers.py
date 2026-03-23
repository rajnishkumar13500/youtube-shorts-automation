"""
Helper functions for YouTube Shorts Automation.
Provides logging setup, file path management, and utility functions.
"""

import logging
import re
from pathlib import Path
from typing import Optional

# Configure logging
def setup_logging(name: str = "youtube_shorts", level: int = logging.INFO) -> logging.Logger:
    """
    Set up and return a logger with consistent formatting.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def clean_script_for_voice(script: str) -> str:
    """
    Remove emotional marker brackets from script for voice generation.
    
    Args:
        script: Original script with emotional markers
    
    Returns:
        Cleaned script without bracket markers
    """
    # Remove all bracket markers like [slow], [pause], [intense]
    cleaned = re.sub(r"\s*\[.*?\]\s*", " ", script)
    # Clean up multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def get_output_path(filename: str, directory: Optional[Path] = None) -> Path:
    """
    Get a safe output path, handling filename conflicts.
    
    Args:
        filename: Desired filename
        directory: Output directory (default: config.OUTPUT_DIR)
    
    Returns:
        Path object for the output file
    """
    if directory is None:
        from config import OUTPUT_DIR
    else:
        OUTPUT_DIR = directory
    
    path = OUTPUT_DIR / filename
    
    # Handle filename conflicts
    if path.exists():
        stem = path.stem
        suffix = path.suffix
        counter = 1
        while path.exists():
            path = OUTPUT_DIR / f"{stem}_{counter}{suffix}"
            counter += 1
    
    return path


def validate_api_key(api_key: Optional[str], api_name: str) -> bool:
    """
    Validate that an API key exists and is not empty.
    
    Args:
        api_key: The API key to validate
        api_name: Name of the API for error messages
    
    Returns:
        True if valid, raises ValueError if invalid
    """
    if not api_key or not api_key.strip():
        raise ValueError(f"{api_name} is not configured. Please set the environment variable.")
    return True

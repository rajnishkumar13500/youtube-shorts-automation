"""
Utility functions for YouTube Shorts Automation.
Includes logging setup, file path management, and error handling helpers.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


# ============================================================================
# Logging Configuration
# ============================================================================

def setup_logging(
    log_level: int = logging.INFO,
    log_dir: Optional[str] = None,
    module_name: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        log_level: Minimum level to log (default: INFO)
        log_dir: Directory to save log files (default: None, no file logging)
        module_name: Name of the module for logger identification
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger_name = module_name if module_name else "youtube_shorts"
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatter with timestamps
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{logger_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# ============================================================================
# Module Loggers
# ============================================================================

# Create loggers for each module
logger_script_generator = setup_logging(module_name="script_generator")
logger_voice_generator = setup_logging(module_name="voice_generator")
logger_image_generator = setup_logging(module_name="image_generator")
logger_video_editor = setup_logging(module_name="video_editor")
logger_main = setup_logging(module_name="main")


# ============================================================================
# Progress Logging Functions
# ============================================================================

def log_pipeline_start(logger: logging.Logger, pipeline_name: str) -> None:
    """
    Log the start of a pipeline step.
    
    Args:
        logger: Logger instance to use
        pipeline_name: Name of the pipeline step
    """
    logger.info("=" * 60)
    logger.info(f"Starting pipeline: {pipeline_name}")
    logger.info("=" * 60)


def log_pipeline_step(logger: logging.Logger, step_name: str, details: str = "") -> None:
    """
    Log a pipeline step with optional details.
    
    Args:
        logger: Logger instance to use
        step_name: Name of the current step
        details: Optional details about the step
    """
    logger.info(f"[STEP] {step_name}")
    if details:
        logger.info(f"       {details}")


def log_pipeline_complete(logger: logging.Logger, pipeline_name: str, duration: Optional[float] = None) -> None:
    """
    Log the completion of a pipeline step.
    
    Args:
        logger: Logger instance to use
        pipeline_name: Name of the pipeline step
        duration: Optional duration in seconds
    """
    logger.info("=" * 60)
    logger.info(f"Completed pipeline: {pipeline_name}")
    if duration is not None:
        logger.info(f"Duration: {duration:.2f} seconds")
    logger.info("=" * 60)


def log_progress(logger: logging.Logger, current: int, total: int, description: str = "") -> None:
    """
    Log progress with percentage.
    
    Args:
        logger: Logger instance to use
        current: Current progress count
        total: Total count
        description: Optional description
    """
    percentage = (current / total) * 100 if total > 0 else 0
    logger.info(f"[PROGRESS] {description} {current}/{total} ({percentage:.1f}%)")


# ============================================================================
# Error Logging with Context
# ============================================================================

def log_error_with_context(
    logger: logging.Logger,
    error: Exception,
    context: dict,
    operation: str = "operation"
) -> None:
    """
    Log an error with additional context information.
    
    Args:
        logger: Logger instance to use
        error: The exception that occurred
        context: Dictionary containing error context (e.g., parameters, state)
        operation: Description of the operation that failed
    """
    logger.error(f"Error during {operation}: {str(error)}")
    logger.error("Context:")
    for key, value in context.items():
        logger.error(f"  {key}: {value}")


def log_api_error(
    logger: logging.Logger,
    api_name: str,
    endpoint: str,
    status_code: Optional[int] = None,
    response: Optional[dict] = None
) -> None:
    """
    Log API-related errors with detailed context.
    
    Args:
        logger: Logger instance to use
        api_name: Name of the API (e.g., OpenAI, ElevenLabs)
        endpoint: API endpoint that failed
        status_code: HTTP status code if available
        response: Response body if available
    """
    logger.error(f"API Error: {api_name}")
    logger.error(f"Endpoint: {endpoint}")
    if status_code:
        logger.error(f"Status Code: {status_code}")
    if response:
        logger.error(f"Response: {response}")


# ============================================================================
# File Path Management
# ============================================================================

def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, create it if necessary.
    
    Args:
        path: Directory path to ensure
    
    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_output_path(filename: str, output_dir: str = "output") -> str:
    """
    Get full output path for a file.
    
    Args:
        filename: Name of the file
        output_dir: Base output directory
    
    Returns:
        Full path to the output file
    """
    return os.path.join(output_dir, filename)


# ============================================================================
# Utility Functions
# ============================================================================

def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted duration string (e.g., "1m 30s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60
    if remaining_seconds == 0:
        return f"{minutes}m"
    return f"{minutes}m {remaining_seconds:.0f}s"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: Numerator
        denominator: Denominator
        default: Value to return if denominator is zero
    
    Returns:
        Result of division or default value
    """
    return numerator / denominator if denominator != 0 else default

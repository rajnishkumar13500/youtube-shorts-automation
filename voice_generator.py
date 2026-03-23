"""
Voice Generator Module.
Uses ElevenLabs API to generate voiceovers from scripts.
Uses Whisper AI to extract precise word timestamps for perfect sync.
Supports multiple API keys with automatic fallback.
"""

import logging
import os
import re
import requests
import json
from pathlib import Path
from typing import Optional, List, Dict

from utils.helpers import logger_voice_generator
from config import ELEVENLABS_API_KEY, DEFAULT_VOICE_ID, VOICE_STABILITY, VOICE_SIMILARITY_BOOST


# ============================================================================
# Multi-Token Management
# ============================================================================

class ElevenLabsTokenManager:
    """Manage multiple ElevenLabs API tokens with automatic fallback."""
    
    def __init__(self):
        """Initialize token manager with tokens from environment."""
        self.tokens = self._load_tokens()
        self.current_token_index = 0
        
        if not self.tokens:
            raise RuntimeError("No ElevenLabs API tokens configured")
        
        logger_voice_generator.info(f"Loaded {len(self.tokens)} ElevenLabs API token(s)")
    
    def _load_tokens(self) -> List[str]:
        """Load API tokens from environment variables."""
        tokens = []
        
        # Load primary token
        if ELEVENLABS_API_KEY:
            tokens.append(ELEVENLABS_API_KEY)
        
        # Load fallback tokens (ELEVENLABS_API_KEY_2, ELEVENLABS_API_KEY_3, etc.)
        i = 2
        while True:
            token = os.getenv(f'ELEVENLABS_API_KEY_{i}')
            if token:
                tokens.append(token)
                i += 1
            else:
                break
        
        return tokens
    
    def get_current_token(self) -> str:
        """Get the current active token."""
        return self.tokens[self.current_token_index]
    
    def switch_to_next_token(self) -> bool:
        """
        Switch to the next available token.
        
        Returns:
            True if switched successfully, False if no more tokens available
        """
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
            logger_voice_generator.warning(
                f"Switching to fallback token #{self.current_token_index + 1}"
            )
            return True
        else:
            logger_voice_generator.error("All ElevenLabs API tokens exhausted")
            return False
    
    def reset(self):
        """Reset to the first token."""
        self.current_token_index = 0
        logger_voice_generator.info("Reset to primary token")
    
    def get_token_info(self) -> str:
        """Get current token info for logging."""
        return f"Token {self.current_token_index + 1}/{len(self.tokens)}"


# Global token manager instance
_token_manager = None


def get_token_manager() -> ElevenLabsTokenManager:
    """Get or create the global token manager."""
    global _token_manager
    if _token_manager is None:
        _token_manager = ElevenLabsTokenManager()
    return _token_manager


# ============================================================================
# Voice Generation with ElevenLabs (Multi-Token Support)
# ============================================================================

def generate_voice(
    script: str,
    output_path: str,
    voice_id: Optional[str] = None,
    stability: Optional[float] = None,
    similarity_boost: Optional[float] = None,
    max_retries: int = None
) -> str:
    """
    Generate voiceover using ElevenLabs API with automatic token fallback.
    SIMPLIFIED: Just generates clean audio without emotional markers.
    
    Args:
        script: The script to convert to voice
        output_path: Path to save the audio file
        voice_id: ElevenLabs voice ID (default from config)
        stability: Voice stability 0.0-1.0 (default from config)
        similarity_boost: Similarity boost 0.0-1.0 (default from config)
        max_retries: Maximum retry attempts (default: number of tokens)
    
    Returns:
        Path to the generated audio file
    
    Raises:
        RuntimeError: If all API tokens fail
    """
    logger_voice_generator.info("=" * 80)
    logger_voice_generator.info("VOICE GENERATION LOG (SIMPLIFIED)")
    logger_voice_generator.info("=" * 80)
    logger_voice_generator.info(f"Generating voice for script (length: {len(script)} chars)")
    logger_voice_generator.info(f"Output path: {output_path}")
    
    # Get token manager
    token_manager = get_token_manager()
    
    # Use defaults if not provided
    voice_id = voice_id or DEFAULT_VOICE_ID
    stability = stability if stability is not None else VOICE_STABILITY
    similarity_boost = similarity_boost if similarity_boost is not None else VOICE_SIMILARITY_BOOST
    max_retries = max_retries or len(token_manager.tokens)
    
    logger_voice_generator.info(f"Using voice ID: {voice_id}")
    logger_voice_generator.info(f"Stability: {stability}, Similarity boost: {similarity_boost}")
    
    # SIMPLIFIED: Clean the script before sending to ElevenLabs
    clean_script = clean_script_for_voice(script)
    logger_voice_generator.info(f"Clean script: {clean_script[:150]}...")
    
    # Try each token until success
    for attempt in range(max_retries):
        api_key = token_manager.get_current_token()
        token_info = token_manager.get_token_info()
        
        logger_voice_generator.info(f"Attempt {attempt + 1}/{max_retries} using {token_info}")
        
        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        
        payload = {
            "text": clean_script,  # SIMPLIFIED: Use clean script
            "model_id": "eleven_multilingual_v2",  # Supports Hinglish
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": 0.5,  # Balanced style
                "use_speaker_boost": True  # Enhance voice clarity
            }
        }
        
        try:
            logger_voice_generator.info(f"Calling ElevenLabs API with {token_info}...")
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            if response.status_code == 200:
                # Success! Save audio file
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                logger_voice_generator.info(f"✓ Audio saved successfully: {output_path}")
                logger_voice_generator.info(f"✓ File size: {file_size / 1024:.2f} KB")
                logger_voice_generator.info(f"✓ Used {token_info}")
                logger_voice_generator.info("=" * 80)
                
                return output_path
            
            elif response.status_code == 401:
                # Invalid API key
                logger_voice_generator.error(f"✗ Invalid API key for {token_info}")
                if not token_manager.switch_to_next_token():
                    raise RuntimeError("All ElevenLabs API tokens are invalid")
                continue
            
            elif response.status_code == 429:
                # Rate limit or quota exceeded
                logger_voice_generator.warning(f"✗ Quota exceeded for {token_info}")
                if not token_manager.switch_to_next_token():
                    raise RuntimeError("All ElevenLabs API tokens have exceeded their quota")
                continue
            
            else:
                # Other error
                error_msg = f"ElevenLabs API error (Status {response.status_code}): {response.text}"
                logger_voice_generator.error(error_msg)
                
                # Try next token for server errors (5xx)
                if response.status_code >= 500:
                    if not token_manager.switch_to_next_token():
                        raise RuntimeError(f"All tokens failed: {error_msg}")
                    continue
                else:
                    # Client error (4xx) - don't retry with other tokens
                    raise RuntimeError(error_msg)
        
        except requests.exceptions.Timeout:
            logger_voice_generator.error(f"✗ Request timeout for {token_info}")
            if not token_manager.switch_to_next_token():
                raise RuntimeError("All ElevenLabs API tokens timed out")
            continue
        
        except requests.exceptions.RequestException as e:
            logger_voice_generator.error(f"✗ Request failed for {token_info}: {e}")
            if not token_manager.switch_to_next_token():
                raise RuntimeError(f"All tokens failed: {e}")
            continue
    
    # All attempts failed
    raise RuntimeError(f"Failed to generate voice after {max_retries} attempts with all available tokens")


def clean_script_for_voice(script: str) -> str:
    """
    Clean script by removing emotional markers and extra formatting.
    SIMPLIFIED: Just basic cleaning.
    
    Args:
        script: Original script with markers
    
    Returns:
        Cleaned script
    """
    logger_voice_generator.info("Cleaning script for voice generation...")
    
    # Remove emotional markers
    cleaned = re.sub(r'\[(slow|pause|intense|excited|calm|whisper)\]', '', script)
    
    # Remove quotes
    cleaned = cleaned.strip('"\'')
    
    # Clean up extra spaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    logger_voice_generator.info(f"Cleaned script length: {len(cleaned)} chars")
    
    return cleaned


def extract_emotional_markers(script: str) -> List[Dict[str, any]]:
    """
    DEPRECATED: Emotional markers removed for simplicity.
    Returns empty list.
    """
    return []


def get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file in seconds.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Duration in seconds
    """
    logger_voice_generator.info("=" * 80)
    logger_voice_generator.info("AUDIO DURATION LOG")
    logger_voice_generator.info("=" * 80)
    logger_voice_generator.info(f"Audio file: {audio_path}")
    
    try:
        import subprocess
        import json
        
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            logger_voice_generator.info(f"✓ Audio duration: {duration:.2f} seconds")
            logger_voice_generator.info("=" * 80)
            return duration
        else:
            logger_voice_generator.warning("Could not determine audio duration")
            logger_voice_generator.info("=" * 80)
            return 15.0  # Default fallback
            
    except Exception as e:
        logger_voice_generator.warning(f"Error getting audio duration: {e}")
        logger_voice_generator.info("=" * 80)
        return 15.0  # Default fallback


# ============================================================================
# Voice ID Helpers
# ============================================================================

def get_word_timestamps_from_audio(audio_path: str) -> List[Dict[str, any]]:
    """
    Extract precise word-level timestamps from audio using Whisper AI.
    This provides ACCURATE timing for perfect subtitle sync.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        List of dicts with 'word', 'start', 'end' for each word
    """
    logger_voice_generator.info("=" * 80)
    logger_voice_generator.info("WHISPER TRANSCRIPTION (FOR SUBTITLES)")
    logger_voice_generator.info("=" * 80)
    
    try:
        import whisper
        
        # Load Whisper model (base is fast and accurate enough)
        logger_voice_generator.info("Loading Whisper model...")
        model = whisper.load_model("base")
        
        # Transcribe with word timestamps
        logger_voice_generator.info(f"Transcribing audio: {audio_path}")
        result = model.transcribe(
            audio_path,
            word_timestamps=True,
            language="hi"  # Hindi/Hinglish
        )
        
        # Extract word-level timestamps
        word_timestamps = []
        full_transcription = []
        
        for segment in result.get('segments', []):
            for word_info in segment.get('words', []):
                word_timestamps.append({
                    'word': word_info['word'].strip(),
                    'start': word_info['start'],
                    'end': word_info['end']
                })
                
                full_transcription.append(word_info['word'].strip())
        
        # Log full transcription
        transcription_text = ' '.join(full_transcription)
        logger_voice_generator.info(f"Transcription ({len(full_transcription)} words):")
        logger_voice_generator.info(f"  {transcription_text[:200]}...")
        
        logger_voice_generator.info(f"✓ Extracted {len(word_timestamps)} word timestamps")
        logger_voice_generator.info("=" * 80)
        
        return word_timestamps
        
    except ImportError:
        logger_voice_generator.error("Whisper not installed. Install with: pip install openai-whisper")
        logger_voice_generator.warning("Falling back to simple timing")
        return []
    except Exception as e:
        logger_voice_generator.error(f"Failed to extract word timestamps: {e}")
        logger_voice_generator.warning("Falling back to simple timing")
        return []


def group_words_into_sentences(word_timestamps: List[Dict], script: str, audio_duration: float) -> List[Dict[str, any]]:
    """
    Group word timestamps into sentences for subtitle synchronization.
    FOCUSED: Only for subtitles, not for images.
    FIXED: Adds delay to compensate for Whisper timing being too fast.
    
    Args:
        word_timestamps: List of word timestamp dicts from Whisper
        script: Original script text
        audio_duration: Total audio duration in seconds
    
    Returns:
        List of sentence dicts with 'text', 'start', 'end', 'duration'
    """
    logger_voice_generator.info("=" * 80)
    logger_voice_generator.info("GROUPING WORDS INTO SENTENCES (FOR SUBTITLES)")
    logger_voice_generator.info("=" * 80)
    
    if not word_timestamps:
        logger_voice_generator.warning("No word timestamps provided")
        return []
    
    # CRITICAL FIX: Add delay to compensate for Whisper being too fast
    # Whisper often gives timestamps that are ahead of actual speech
    from config import SUBTITLE_DELAY
    
    logger_voice_generator.info(f"Applying subtitle delay: {SUBTITLE_DELAY}s to sync with audio")
    
    # Clean script and split into sentences
    clean_script = re.sub(r'\[(slow|pause|intense|excited|calm|whisper)\]', '', script)
    clean_script = clean_script.strip('"\'')
    sentences = re.split(r'(?<=[.!?])\s+', clean_script)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    logger_voice_generator.info(f"Script has {len(sentences)} sentences")
    logger_voice_generator.info(f"Whisper provided {len(word_timestamps)} word timestamps")
    
    sentence_timings = []
    word_index = 0
    
    for i, sentence in enumerate(sentences):
        # Count words in this sentence
        sentence_words = sentence.split()
        num_words = len(sentence_words)
        
        # Check if we have enough timestamps
        if word_index >= len(word_timestamps):
            logger_voice_generator.warning(f"Sentence {i+1}: No more timestamps, stopping")
            break
        
        # Get available words
        available_words = len(word_timestamps) - word_index
        if num_words > available_words:
            logger_voice_generator.warning(
                f"Sentence {i+1}: Need {num_words} words but only {available_words} available"
            )
            num_words = available_words
        
        if num_words > 0:
            # Get timestamps for this sentence
            sentence_word_timestamps = word_timestamps[word_index:word_index + num_words]
            
            if sentence_word_timestamps:
                # Get Whisper's timing and ADD DELAY
                whisper_start = sentence_word_timestamps[0]['start']
                whisper_end = sentence_word_timestamps[-1]['end']
                
                # Apply delay to sync with actual audio
                start_time = whisper_start + SUBTITLE_DELAY
                end_time = whisper_end + SUBTITLE_DELAY
                
                # Ensure valid duration
                if end_time <= start_time:
                    end_time = start_time + 0.5
                
                # Don't exceed audio duration
                if end_time > audio_duration:
                    end_time = audio_duration
                
                # Ensure start time is not negative
                if start_time < 0:
                    start_time = 0
                
                sentence_timings.append({
                    'text': sentence,
                    'start': start_time,
                    'end': end_time,
                    'duration': end_time - start_time
                })
                
                logger_voice_generator.info(
                    f"✓ Sentence {i+1}: {start_time:.2f}s - {end_time:.2f}s (delayed by {SUBTITLE_DELAY}s) | {sentence[:50]}..."
                )
                
                word_index += num_words
    
    # Extend last sentence to cover full audio
    if sentence_timings and sentence_timings[-1]['end'] < audio_duration - 0.1:
        old_end = sentence_timings[-1]['end']
        sentence_timings[-1]['end'] = audio_duration
        sentence_timings[-1]['duration'] = audio_duration - sentence_timings[-1]['start']
        logger_voice_generator.info(f"Extended last sentence from {old_end:.2f}s to {audio_duration:.2f}s")
    
    logger_voice_generator.info(f"✓ Created {len(sentence_timings)} sentence timings with {SUBTITLE_DELAY}s delay")
    logger_voice_generator.info("=" * 80)
    
    return sentence_timings


def list_available_voices() -> list:
    """
    List available voices from ElevenLabs.
    
    Returns:
        List of voice dictionaries with id, name, and description
    """
    if not ELEVENLABS_API_KEY:
        logger_voice_generator.error("ElevenLabs API key not configured")
        return []
    
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            voices = response.json().get('voices', [])
            logger_voice_generator.info(f"Found {len(voices)} available voices")
            return voices
        else:
            logger_voice_generator.error(f"Failed to list voices: {response.status_code}")
            return []
    except Exception as e:
        logger_voice_generator.error(f"Error listing voices: {e}")
        return []

"""
Video Editor Module.
Uses FFmpeg to create final videos from images and audio.
"""

import logging
import os
import re
import subprocess
from datetime import timedelta
from typing import List, Tuple, Dict

from utils.helpers import logger_video_editor
from config import OUTPUT_DIR


# ============================================================================
# SRT Format Helper Functions
# ============================================================================

def format_srt_time(seconds: float) -> str:
    """
    Convert seconds to SRT time format (HH:MM:SS,mmm).
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"


def split_script_into_phrases(script: str, max_duration: float = 2.0) -> List[Tuple[str, float, float]]:
    """
    Split script into short phrases suitable for subtitles.
    
    Args:
        script: The script text
        max_duration: Maximum duration per phrase in seconds
    
    Returns:
        List of (text, start_time, end_time) tuples
    """
    # Split script into sentences
    sentences = re.split(r'(?<=[.!?])\s+', script)
    
    phrases = []
    current_phrase = ""
    current_start = 0.0
    current_duration = 0.0
    
    for sentence in sentences:
        # Clean up the sentence
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Check if adding this sentence would exceed max duration
        # Estimate reading speed: ~3 words per second
        word_count = len(sentence.split())
        estimated_duration = word_count / 3.0
        
        if len(current_phrase) > 0 and (current_duration + estimated_duration > max_duration or len(current_phrase.split()) > 8):
            # Save current phrase
            phrases.append((current_phrase.strip(), current_start, current_start + current_duration))
            current_phrase = sentence
            current_start = current_start + current_duration
            current_duration = estimated_duration
        else:
            # Add to current phrase
            if current_phrase:
                current_phrase += " " + sentence
            else:
                current_phrase = sentence
            current_duration = estimated_duration
    
    # Don't forget the last phrase
    if current_phrase:
        phrases.append((current_phrase.strip(), current_start, current_start + current_duration))
    
    return phrases


def bold_words_in_text(text: str, keywords: List[str] = None) -> str:
    """
    Add bold formatting to important words in text.
    
    Args:
        text: Original text
        keywords: List of keywords to bold (optional)
    
    Returns:
        Text with bold formatting
    """
    if keywords is None:
        # Default: bold first word of each sentence and important words
        words = text.split()
        if len(words) > 0:
            words[0] = f"<b>{words[0]}</b>"
        return " ".join(words)
    else:
        # Bold specified keywords
        result = text
        for keyword in keywords:
            result = re.sub(r'\b' + re.escape(keyword) + r'\b', f'<b>{keyword}</b>', result, flags=re.IGNORECASE)
        return result


def style_subtitle_text(text: str) -> str:
    """
    Add creative styling to subtitle text for visual appeal.
    Makes subtitles more engaging with bold emphasis (NO color codes in text).
    
    Args:
        text: Original subtitle text
    
    Returns:
        Styled text with formatting (bold only, no color codes visible)
    """
    # Remove any emotional markers that might have slipped through
    text = re.sub(r'\[(slow|pause|intense|excited|calm|whisper)\]', '', text)
    
    # Remove any quotes at the beginning/end
    text = text.strip('"\'')
    
    # Important keywords to emphasize (health/fitness related)
    emphasis_words = [
        'day', 'energy', 'fat', 'burn', 'spike', 'explode', 'clear', 'amazing',
        'weight', 'skin', 'body', 'health', 'power', 'boost', 'transform',
        'sugar', 'free', 'start', 'shuru', 'karein', 'hoga', 'kya', 'din',
        'paani', 'water', 'like', 'subscribe', 'follow'
    ]
    
    # Split into words
    words = text.split()
    styled_words = []
    
    for i, word in enumerate(words):
        word_lower = word.lower().strip('!?.,')
        
        # First word - always bold
        if i == 0:
            styled_words.append(f'<b>{word}</b>')
        # Important keywords - bold
        elif any(keyword in word_lower for keyword in emphasis_words):
            styled_words.append(f'<b>{word}</b>')
        # Numbers - bold
        elif re.search(r'\d+', word):
            styled_words.append(f'<b>{word}</b>')
        # Exclamation words - bold
        elif word.endswith('!'):
            styled_words.append(f'<b>{word}</b>')
        else:
            styled_words.append(word)
    
    return ' '.join(styled_words)


def generate_subtitles(
    script: str,
    audio_duration: float,
    output_path: str = None,
    sentence_timings: List[Dict] = None,
    emotional_markers: List[Dict] = None
) -> str:
    """
    Generate SRT subtitle file with timing.
    Uses Whisper AI timestamps if available for PERFECT synchronization.
    Falls back to simple timing if Whisper is not available.
    
    Args:
        script: The script text
        audio_duration: ACTUAL duration of the audio file in seconds
        output_path: Path to save subtitles file (default: output/subtitles.srt)
        sentence_timings: Optional precise timings from Whisper AI
        emotional_markers: DEPRECATED (ignored)
    
    Returns:
        Path to the generated subtitles file
    """
    logger_video_editor.info("=" * 80)
    logger_video_editor.info("SUBTITLE GENERATION")
    logger_video_editor.info("=" * 80)
    
    if output_path is None:
        output_path = os.path.join(OUTPUT_DIR, "subtitles.srt")
    
    try:
        # Use Whisper timings if available
        if sentence_timings:
            logger_video_editor.info(f"✓ Using Whisper-based precise timing ({len(sentence_timings)} sentences)")
            
            srt_lines = []
            
            for i, timing in enumerate(sentence_timings):
                text = timing.get('text', '')
                start_time = timing['start']
                end_time = timing['end']
                
                # Ensure valid timing
                if end_time <= start_time:
                    end_time = start_time + 0.5
                
                if end_time > audio_duration:
                    end_time = audio_duration
                
                # Style the text
                styled_text = style_subtitle_text(text)
                
                logger_video_editor.info(f"Subtitle {i+1}: {start_time:.2f}s - {end_time:.2f}s | {text[:50]}...")
                
                # Format SRT entry
                srt_lines.append(str(i + 1))
                srt_lines.append(f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}")
                srt_lines.append(styled_text)
                srt_lines.append("")  # Empty line
            
            # Write SRT file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(srt_lines))
            
            logger_video_editor.info(f"✓ Subtitles generated with Whisper timing: {output_path}")
            logger_video_editor.info(f"✓ Total subtitles: {len(sentence_timings)}")
            logger_video_editor.info("=" * 80)
            
            return output_path
        
        # Fallback to simple timing
        else:
            logger_video_editor.info("⚠ Using simple word-count timing (Whisper not available)")
            
            # Clean script - remove emotional markers
            clean_text = re.sub(r'\[(slow|pause|intense|excited|calm|whisper)\]', '', script)
            clean_text = clean_text.strip('"\'')
            
            # Split into sentences for natural subtitle breaks
            sentences = re.split(r'(?<=[.!?])\s+', clean_text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            logger_video_editor.info(f"Split script into {len(sentences)} sentences")
            
            # Calculate total words
            total_words = sum(len(s.split()) for s in sentences)
            
            # Calculate words per second from ACTUAL audio
            words_per_second = total_words / audio_duration if audio_duration > 0 else 3.0
            
            logger_video_editor.info(f"Total words: {total_words}")
            logger_video_editor.info(f"Words per second: {words_per_second:.2f}")
            
            srt_lines = []
            current_time = 0.0
            
            for i, sentence in enumerate(sentences):
                # Style the text
                styled_text = style_subtitle_text(sentence)
                
                # Calculate duration based on word count
                word_count = len(sentence.split())
                sentence_duration = word_count / words_per_second
                
                # Ensure we don't exceed audio duration
                start_time = current_time
                end_time = min(current_time + sentence_duration, audio_duration)
                
                logger_video_editor.info(f"Subtitle {i+1}: {start_time:.2f}s - {end_time:.2f}s ({word_count} words)")
                
                # Format SRT entry
                srt_lines.append(str(i + 1))
                srt_lines.append(f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}")
                srt_lines.append(styled_text)
                srt_lines.append("")  # Empty line
                
                current_time = end_time
            
            # Write SRT file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(srt_lines))
            
            logger_video_editor.info(f"✓ Subtitles generated with simple timing: {output_path}")
            logger_video_editor.info(f"✓ Total subtitles: {len(sentences)}")
            logger_video_editor.info("=" * 80)
            
            return output_path
        
    except Exception as e:
        logger_video_editor.error(f"Failed to generate subtitles: {e}")
        raise RuntimeError(f"Failed to generate subtitles: {e}")


def add_subtitles(
    video_path: str,
    subtitles_path: str,
    output_path: str,
    subtitle_color: str = "yellow",
    emotional_markers: List[Dict] = None
) -> str:
    """
    Add professional subtitles to video using FFmpeg with single consistent font.
    Ensures subtitles are positioned at BOTTOM CENTER and fully visible.
    SIMPLIFIED: No emotional markers.
    
    Args:
        video_path: Path to input video
        subtitles_path: Path to subtitles file
        output_path: Path for output video
        subtitle_color: Color for subtitles (yellow, white, cyan, etc.)
        emotional_markers: DEPRECATED (ignored)
    
    Returns:
        Path to the video with subtitles
    """
    logger_video_editor.info("=" * 80)
    logger_video_editor.info("SUBTITLE BURNING (SIMPLIFIED)")
    logger_video_editor.info("=" * 80)
    logger_video_editor.info(f"Adding professional subtitles (color: {subtitle_color})")
    logger_video_editor.info(f"Input video: {video_path}")
    logger_video_editor.info(f"Subtitles file: {subtitles_path}")
    logger_video_editor.info(f"Output video: {output_path}")
    
    # Color mapping (ASS format uses BGR, not RGB)
    color_map = {
        "yellow": "&H00FFFF",    # Yellow (BGR format)
        "white": "&H00FFFFFF",   # White
        "cyan": "&H00FFFF00",    # Cyan
        "orange": "&H0000A5FF",  # Orange
        "green": "&H0000FF00",   # Green
    }
    
    primary_color = color_map.get(subtitle_color.lower(), "&H00FFFF")
    
    try:
        # Escape Windows paths for FFmpeg
        subtitles_path_escaped = subtitles_path.replace('\\', '/').replace(':', '\\:')
        
        # Small subtitle style - BOTTOM CENTER positioning
        # Alignment values: 1=left, 2=center, 3=right (bottom row)
        subtitle_style = (
            "FontName=Arial,"              # Use Arial (clean and readable)
            "FontSize=14,"                 # Small font size as requested
            "PrimaryColour=" + primary_color + ","
            "OutlineColour=&H00000000,"    # Black outline
            "BackColour=&H80000000,"       # Semi-transparent black background
            "Bold=1,"                      # Bold text
            "Outline=2,"                   # Outline for contrast
            "Shadow=1,"                    # Subtle shadow
            "Alignment=2,"                 # Bottom center
            "MarginV=20,"                  # 20 pixels from bottom (small space)
            "MarginL=30,"                  # 30 pixels from left
            "MarginR=30"                   # 30 pixels from right
        )
        
        logger_video_editor.info(f"Subtitle style: {subtitle_style}")
        
        ffmpeg_command = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vf', f"subtitles='{subtitles_path_escaped}':force_style='{subtitle_style}'",
            '-c:a', 'copy',
            '-preset', 'fast',
            output_path
        ]
        
        logger_video_editor.debug(f"FFmpeg command: {' '.join(ffmpeg_command)}")
        
        result = subprocess.run(
            ffmpeg_command,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode != 0:
            logger_video_editor.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
        
        logger_video_editor.info("✓ Professional subtitles added successfully")
        logger_video_editor.info(f"✓ Output video: {output_path}")
        logger_video_editor.info("=" * 80)
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        logger_video_editor.error(f"FFmpeg command failed: {e}")
        raise RuntimeError(f"Failed to add subtitles: {e}")
    except subprocess.TimeoutExpired:
        logger_video_editor.error("FFmpeg subtitle burning timeout")
        raise RuntimeError("Subtitle burning timeout - video may be too long")
    except Exception as e:
        logger_video_editor.error(f"Failed to add subtitles: {e}")
        raise RuntimeError(f"Failed to add subtitles: {e}")


def create_video(
    images: list,
    audio_path: str,
    output_path: str,
    image_timings: list = None,
    bg_music_path: str = None,
    bg_music_volume: float = 0.3,
    emotional_markers: List[Dict] = None
) -> str:
    """
    Create final video from images and audio with Ken Burns effect and transitions.
    SIMPLIFIED: Uses simple equal-interval timing for images.
    
    Args:
        images: List of image paths
        audio_path: Path to audio file
        output_path: Path for output video
        image_timings: List of dicts with timing info (optional)
        bg_music_path: Optional path to background music file
        bg_music_volume: Volume level for background music (0.0 to 1.0)
        emotional_markers: DEPRECATED (ignored)
    
    Returns:
        Path to the generated video
    """
    logger_video_editor.info("=" * 80)
    logger_video_editor.info("VIDEO CREATION (SIMPLIFIED)")
    logger_video_editor.info("=" * 80)
    logger_video_editor.info(f"Creating video from {len(images)} images")
    logger_video_editor.info(f"Audio: {audio_path}")
    logger_video_editor.info(f"Output: {output_path}")
    
    if not images:
        raise RuntimeError("No images provided for video creation")
    
    if not os.path.exists(audio_path):
        raise RuntimeError(f"Audio file not found: {audio_path}")
    
    # Get audio duration
    audio_duration = get_audio_duration(audio_path)
    logger_video_editor.info(f"Audio duration: {audio_duration:.2f} seconds")
    
    # Use timing information if provided, otherwise calculate equal intervals
    if image_timings and len(image_timings) == len(images):
        logger_video_editor.info("Using provided timing for images")
        for i, timing in enumerate(image_timings):
            logger_video_editor.info(
                f"Image {i+1}: {timing.get('start_time', 0):.2f}s - {timing.get('end_time', 0):.2f}s "
                f"({timing.get('duration', 0):.2f}s)"
            )
    else:
        logger_video_editor.info("Using equal interval timing for images")
        duration_per_image = audio_duration / len(images)
        image_timings = []
        for i in range(len(images)):
            start_time = i * duration_per_image
            end_time = min((i + 1) * duration_per_image, audio_duration)
            image_timings.append({
                'start_time': start_time,
                'end_time': end_time,
                'duration': end_time - start_time
            })
    
    try:
        # Create video with Ken Burns effect and transitions
        temp_video = output_path.replace('.mp4', '_temp.mp4')
        
        # Build FFmpeg filter complex for Ken Burns effect with timing
        filter_complex = build_ken_burns_filter_with_timing(
            images, image_timings, audio_duration
        )
        
        # Create input file list - use audio duration for all images to ensure sync
        input_args = []
        for img in images:
            # Use audio duration + buffer to ensure we have enough frames
            input_args.extend(['-loop', '1', '-t', str(audio_duration + 2), '-i', img])
        
        # Add audio input
        input_args.extend(['-i', audio_path])
        
        # Build complete FFmpeg command with audio as master timing
        ffmpeg_cmd = [
            'ffmpeg', '-y'
        ] + input_args + [
            '-filter_complex', filter_complex,
            '-map', '[outv]',
            '-map', f'{len(images)}:a',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-t', str(audio_duration),  # Force exact audio duration
            temp_video
        ]
        
        logger_video_editor.info("Running FFmpeg to create video with simple timing...")
        logger_video_editor.debug(f"FFmpeg command: {' '.join(ffmpeg_cmd)}")
        
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            logger_video_editor.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
        
        logger_video_editor.info("✓ Video created successfully with simple timing")
        
        # If background music is provided, mix it
        if bg_music_path and os.path.exists(bg_music_path):
            logger_video_editor.info("Mixing background music")
            final_output = output_path
            mix_background_music(temp_video, audio_path, bg_music_path, final_output, bg_music_volume)
            # Clean up temp file
            if os.path.exists(temp_video):
                os.remove(temp_video)
            return final_output
        else:
            # Rename temp to final
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_video, output_path)
            return output_path
        
    except subprocess.TimeoutExpired:
        logger_video_editor.error("FFmpeg timeout")
        raise RuntimeError("Video creation timeout")
    except Exception as e:
        logger_video_editor.error(f"Failed to create video: {e}")
        raise RuntimeError(f"Failed to create video: {e}")


def build_ken_burns_filter_with_timing(
    images: list,
    image_timings: list,
    total_duration: float,
    emotional_markers: List[Dict] = None
) -> str:
    """
    Build FFmpeg filter using SMOOTH CONTINUOUS TIMELINE without visible pauses.
    SIMPLIFIED: No emotional markers, just smooth animations.
    
    Strategy:
    1. Each image gets a SMOOTH Ken Burns effect for its FULL duration
    2. Crossfade transitions between images for seamless flow
    3. Timeline matches audio exactly
    
    Args:
        images: List of image paths
        image_timings: List of dicts with 'start_time', 'end_time', 'duration'
        total_duration: Total video duration (audio duration)
        emotional_markers: DEPRECATED (ignored)
    
    Returns:
        FFmpeg filter_complex string
    """
    filters = []
    num_images = len(images)
    fps = 30
    transition_duration = 0.5  # Crossfade duration
    
    logger_video_editor.info("=" * 80)
    logger_video_editor.info("Building SMOOTH TIMELINE (SIMPLIFIED)")
    logger_video_editor.info("=" * 80)
    
    # Calculate actual display duration for each image (including overlap for transitions)
    for i in range(num_images):
        timing = image_timings[i]
        start_time = timing['start_time']
        end_time = timing['end_time']
        
        # Calculate the full duration this image should be visible
        if i < num_images - 1:
            # Image visible from its start to next image's start
            next_start = image_timings[i + 1]['start_time']
            full_duration = next_start - start_time
        else:
            # Last image extends to end of audio
            full_duration = total_duration - start_time
        
        # Ensure minimum duration
        if full_duration < 0.5:
            full_duration = 0.5
            logger_video_editor.warning(f"Image {i+1}: Duration too short, set to 0.5s")
        
        # Calculate frame count for smooth animation
        total_frames = int(full_duration * fps)
        if total_frames < 1:
            total_frames = 1
        
        logger_video_editor.info(
            f"Image {i+1}/{num_images}: "
            f"start={start_time:.3f}s, "
            f"full_duration={full_duration:.3f}s ({total_frames} frames)"
        )
        
        # Build filter chain for SMOOTH continuous animation
        # 1. Scale and crop to 9:16
        scale_crop = f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        
        # 2. SMOOTH Ken Burns zoom effect across FULL duration (no pauses)
        # Slower zoom rate for smoother, more natural movement
        zoom = f"zoompan=z='min(zoom+0.001,1.08)':d={total_frames}:s=1080x1920:fps={fps}"
        
        # 3. Set PTS for proper timing
        setpts = f"setpts=PTS-STARTPTS"
        
        # 4. Trim to exact duration
        trim = f"trim=duration={full_duration:.6f},setpts=PTS-STARTPTS"
        
        # Combine filters
        filters.append(f"{scale_crop},{zoom},{setpts},{trim}[v{i}]")
        
        logger_video_editor.info(f"  → Smooth Ken Burns animation for {full_duration:.3f}s")
    
    # Create smooth crossfade transitions between images
    if num_images == 1:
        concat_filter = "[v0]"
    elif num_images == 2:
        # Simple crossfade for 2 images
        offset = image_timings[1]['start_time'] - image_timings[0]['start_time'] - transition_duration
        filters.append(
            f"[v0][v1]xfade=transition=fade:duration={transition_duration}:offset={offset}[outv_temp]"
        )
        concat_filter = "[outv_temp]"
    else:
        # Chain crossfades for multiple images
        for i in range(num_images - 1):
            if i == 0:
                # First transition
                offset = image_timings[1]['start_time'] - image_timings[0]['start_time'] - transition_duration
                filters.append(
                    f"[v0][v1]xfade=transition=fade:duration={transition_duration}:offset={offset}[vx1]"
                )
            else:
                # Subsequent transitions
                offset = image_timings[i+1]['start_time'] - image_timings[0]['start_time'] - (i+1) * transition_duration
                filters.append(
                    f"[vx{i}][v{i+1}]xfade=transition=fade:duration={transition_duration}:offset={offset}[vx{i+1}]"
                )
        
        concat_filter = f"[vx{num_images-1}]"
    
    # Final output with format conversion
    all_filters = ';'.join(filters) + f";{concat_filter}format=yuv420p[outv]"
    
    # Validation
    expected_duration = total_duration
    
    logger_video_editor.info("=" * 80)
    logger_video_editor.info(f"✓ SMOOTH filter built")
    logger_video_editor.info(f"✓ Expected duration: {expected_duration:.3f}s (audio: {total_duration:.3f}s)")
    logger_video_editor.info(f"✓ Transition duration: {transition_duration}s")
    logger_video_editor.info("=" * 80)
    
    return all_filters


def build_ken_burns_filter(images: list, duration_per_image: float, total_duration: float) -> str:
    """
    Build FFmpeg filter complex for Ken Burns zoom effect with crossfade transitions.
    Ensures video covers full audio duration by extending the last image.
    
    Args:
        images: List of image paths
        duration_per_image: Duration for each image
        total_duration: Total video duration (audio duration)
    
    Returns:
        FFmpeg filter_complex string
    """
    filters = []
    transition_duration = 0.5  # Crossfade duration in seconds
    
    # Calculate actual duration per image to ensure we cover full audio
    # Last image should extend to fill any remaining time
    num_images = len(images)
    
    # Process each image with Ken Burns effect
    for i in range(num_images):
        # For the last image, extend duration to cover remaining time
        if i == num_images - 1:
            # Calculate remaining time
            time_used = (num_images - 1) * duration_per_image - (num_images - 1) * transition_duration
            remaining_time = total_duration - time_used
            current_duration = max(duration_per_image, remaining_time + 1.0)  # Add 1 second buffer
            logger_video_editor.info(f"Last image duration extended to {current_duration:.2f}s to cover full audio")
        else:
            current_duration = duration_per_image
        
        # Scale to 1080x1920 (9:16) and crop to fit
        scale_filter = f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        
        # Add Ken Burns zoom effect (slow zoom in)
        # Start at 100% scale, end at 110% scale for dynamic feel
        zoom_filter = f"zoompan=z='min(zoom+0.0015,1.1)':d={int(current_duration * 30)}:s=1080x1920:fps=30"
        
        # Add slight fade in/out for smoother transitions
        if i == 0:
            # First image: fade in only
            fade_filter = f"fade=t=in:st=0:d=0.3"
        elif i == num_images - 1:
            # Last image: fade out at the very end
            fade_filter = f"fade=t=out:st={current_duration - 0.5}:d=0.5"
        else:
            # Middle images: fade in and out
            fade_filter = f"fade=t=in:st=0:d=0.3,fade=t=out:st={current_duration - 0.3}:d=0.3"
        
        # Combine filters for this image
        filters.append(f"{scale_filter},{zoom_filter},{fade_filter}[v{i}]")
    
    # Create crossfade transitions between images
    if num_images == 1:
        # Single image, no transitions needed
        concat_filter = "[v0]"
    else:
        # Build crossfade chain
        xfade_chain = []
        for i in range(num_images - 1):
            if i == 0:
                # First transition
                offset = duration_per_image - transition_duration
                xfade_chain.append(
                    f"[v0][v1]xfade=transition=fade:duration={transition_duration}:offset={offset}[vx1]"
                )
            else:
                # Subsequent transitions
                offset = (i + 1) * duration_per_image - (i + 1) * transition_duration
                xfade_chain.append(
                    f"[vx{i}][v{i+1}]xfade=transition=fade:duration={transition_duration}:offset={offset}[vx{i+1}]"
                )
        
        # Join all transitions
        filters.extend(xfade_chain)
        concat_filter = f"[vx{num_images-1}]"
    
    # Final output
    all_filters = ';'.join(filters) + f";{concat_filter}format=yuv420p[outv]"
    
    return all_filters


def get_audio_duration(audio_path: str) -> float:
    """
    Get duration of audio file using FFprobe.
    
    Args:
        audio_path: Path to audio file
    
    Returns:
        Duration in seconds
    """
    try:
        import json
        
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            audio_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            duration = float(data['format']['duration'])
            logger_video_editor.debug(f"Audio duration: {duration:.2f} seconds")
            return duration
        else:
            logger_video_editor.warning("Could not determine audio duration, using default")
            return 15.0
            
    except Exception as e:
        logger_video_editor.warning(f"Error getting audio duration: {e}")
        return 15.0

def mix_background_music(
    video_path: str,
    audio_path: str,
    bg_music_path: str,
    output_path: str,
    bg_music_volume: float = 0.3
) -> str:
    """
    Mix background music with video audio.
    
    Args:
        video_path: Path to input video (with audio)
        audio_path: Path to voice audio file
        bg_music_path: Path to background music file
        output_path: Path for output video with mixed audio
        bg_music_volume: Volume level for background music (0.0 to 1.0)
    
    Returns:
        Path to the video with mixed audio
    """
    logger_video_editor.info("Mixing background music with video")
    logger_video_editor.info(f"Background music: {bg_music_path}")
    logger_video_editor.info(f"Background music volume: {bg_music_volume}")
    
    # Check if background music file exists
    if not os.path.exists(bg_music_path):
        logger_video_editor.warning(f"Background music file not found: {bg_music_path}")
        logger_video_editor.info("Skipping background music mixing")
        return video_path
    
    try:
        # Get audio duration to loop background music if needed
        # Use ffprobe to get audio duration
        import json
        
        probe_command = (
            f'ffprobe -v error -show_entries format=duration '
            f'-of json "{bg_music_path}"'
        )
        
        result = subprocess.run(
            probe_command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger_video_editor.warning(f"Could not get background music duration: {result.stderr}")
            # Fall back to using video duration
            bg_music_duration = None
        else:
            bg_music_duration = float(json.loads(result.stdout)['format']['duration'])
        
        # Build FFmpeg command to mix audio
        # Using amix filter to combine voice audio with background music
        # The background music is looped if shorter than the video
        
        if bg_music_duration is not None and bg_music_duration > 0:
            # Loop background music if needed
            bg_music_filter = (
                f'[1:a]aloop=loop=-1:size=2e+09,atrim=0:{bg_music_duration},'
                f'asetpts=PTS-STARTPTS[a1];'
            )
        else:
            # If we couldn't get duration, just use the file as-is
            bg_music_filter = '[1:a]atrim=0:0.001[a1];'
        
        # Create mixed audio using amix filter
        # voice audio is at 1.0 volume, background music is at bg_music_volume
        mixed_audio_filter = (
            f'[0:a][a1]amix=inputs=2:duration=first:dropout_transition=0,'
            f'volume={1 + bg_music_volume}[outa]'
        )
        
        # Build complete FFmpeg command
        ffmpeg_command = (
            f'ffmpeg -y -i "{video_path}" -i "{bg_music_path}" '
            f'-filter_complex "{bg_music_filter}{mixed_audio_filter}" '
            f'-map 0:v -map "[outa]" '
            f'-c:v copy -c:a aac '
            f'"{output_path}"'
        )
        
        logger_video_editor.debug(f"FFmpeg command: {ffmpeg_command}")
        
        # Execute FFmpeg command
        result = subprocess.run(
            ffmpeg_command,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger_video_editor.error(f"FFmpeg error: {result.stderr}")
            raise RuntimeError(f"Failed to mix background music: {result.stderr}")
        
        logger_video_editor.info("Background music mixed successfully")
        logger_video_editor.info(f"Output video: {output_path}")
        
        return output_path
        
    except subprocess.CalledProcessError as e:
        logger_video_editor.error(f"FFmpeg command failed: {e}")
        raise RuntimeError(f"Failed to mix background music: {e}")
    except Exception as e:
        logger_video_editor.error(f"Failed to mix background music: {e}")
        raise RuntimeError(f"Failed to mix background music: {e}")

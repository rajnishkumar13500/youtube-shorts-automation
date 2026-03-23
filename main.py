"""
Main entry point for YouTube Shorts Automation.
"""

import argparse
import time
from typing import Optional

from config import OUTPUT_DIR, LOGS_DIR, AUDIO_OUTPUT_PATH, IMAGES_DIR, FINAL_VIDEO_PATH
from utils.helpers import (
    setup_logging,
    log_pipeline_start,
    log_pipeline_complete,
    log_pipeline_step,
    log_error_with_context
)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate YouTube Shorts videos using AI"
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Topic for the YouTube Short"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=OUTPUT_DIR,
        help="Output directory for generated files"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Script duration in seconds (15-45, default: 30)"
    )
    parser.add_argument(
        "--bg-music",
        type=str,
        default=None,
        help="Path to background music file (optional)"
    )
    parser.add_argument(
        "--bg-music-volume",
        type=float,
        default=None,
        help="Background music volume (0.0 to 1.0, default from config)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Groq model to use (default: openai/gpt-oss-120b from config)"
    )
    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the YouTube Shorts automation pipeline.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    args = parse_arguments()

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logging(
        log_level=getattr(__import__("logging"), log_level),
        log_dir=LOGS_DIR,
        module_name="main"
    )

    logger.info(f"Starting YouTube Shorts Automation for topic: {args.topic}")
    logger.info(f"Output directory: {args.output_dir}")

    try:
        # Step 1: Generate script
        log_pipeline_step(logger, "Script Generation", f"Topic: {args.topic}")
        from script_generator import generate_script
        from config import DEFAULT_GROQ_MODEL
        model = args.model if args.model else DEFAULT_GROQ_MODEL
        script = generate_script(args.topic, duration=args.duration, model=model)
        logger.info(f"Script generated successfully ({len(script)} characters)")
        logger.info(f"Script: {script}")

        # Step 2: Generate voice
        log_pipeline_step(logger, "Voice Generation", "Generating audio from script")
        from voice_generator import generate_voice, get_audio_duration, get_word_timestamps_from_audio, group_words_into_sentences
        audio_path = AUDIO_OUTPUT_PATH
        generate_voice(script, audio_path)
        audio_duration = get_audio_duration(audio_path)
        logger.info(f"Voice generated successfully: {audio_path}")
        logger.info(f"Audio duration: {audio_duration:.2f} seconds")
        
        # Step 2.5: Extract precise word timestamps using Whisper AI (FOR SUBTITLES ONLY)
        log_pipeline_step(logger, "Whisper Transcription", "Extracting word timestamps for subtitle sync")
        word_timestamps = get_word_timestamps_from_audio(audio_path)
        
        if word_timestamps:
            logger.info(f"✓ Extracted {len(word_timestamps)} word timestamps")
            # Group words into sentences for subtitle timing
            sentence_timings = group_words_into_sentences(word_timestamps, script, audio_duration)
            logger.info(f"✓ Grouped into {len(sentence_timings)} sentences for subtitles")
        else:
            logger.warning("⚠ Whisper not available, using simple timing for subtitles")
            sentence_timings = None

        # Step 3: Generate AI-powered image prompts and images
        log_pipeline_step(logger, "Image Generation", "Creating AI-generated scene prompts")
        from image_generator import generate_ai_image_prompts, generate_images
        logger.info(f"Using Groq AI to generate detailed image prompts for script")
        
        # SIMPLE: Use equal-interval timing for images (not Whisper)
        logger.info("Using simple equal-interval timing for images")
        image_prompts = generate_ai_image_prompts(script, audio_duration, topic=args.topic)
        
        logger.info(f"Generated {len(image_prompts)} AI-powered image prompts")
        image_paths = generate_images(image_prompts, IMAGES_DIR)
        logger.info(f"Generated {len(image_paths)} professional images")

        # Step 4: Create video
        log_pipeline_step(logger, "Video Creation", "Combining images and audio")
        from video_editor import create_video
        video_path = FINAL_VIDEO_PATH
        bg_music_path = args.bg_music if args.bg_music else None
        bg_music_volume = args.bg_music_volume if args.bg_music_volume is not None else 0.3
        
        # SIMPLE: Use equal-interval timing for images
        logger.info("Creating video with simple equal-interval timing for images")
        create_video(
            images=image_paths,
            audio_path=audio_path,
            output_path=video_path,
            image_timings=image_prompts,
            bg_music_path=bg_music_path,
            bg_music_volume=bg_music_volume
        )
        logger.info(f"Video created successfully: {video_path}")

        # Step 5: Add subtitles
        log_pipeline_step(logger, "Subtitles", "Adding subtitles to video")
        from video_editor import generate_subtitles, add_subtitles
        
        # WHISPER: Use Whisper timing for subtitles if available
        if sentence_timings:
            logger.info(f"✓ Generating subtitles with Whisper-based precise timing")
            subtitles_path = generate_subtitles(script, audio_duration, sentence_timings=sentence_timings)
        else:
            logger.info(f"⚠ Generating subtitles with simple timing (Whisper not available)")
            subtitles_path = generate_subtitles(script, audio_duration)
        
        final_video_path = video_path.replace('.mp4', '_final.mp4')
        logger.info(f"Burning subtitles into video")
        add_subtitles(video_path, subtitles_path, final_video_path)
        logger.info(f"Final video with subtitles: {final_video_path}")

        log_pipeline_complete(logger, "YouTube Shorts Generation", duration=0)
        logger.info("Pipeline completed successfully!")

        return 0

    except Exception as e:
        log_error_with_context(
            logger=logger,
            error=e,
            context={"topic": args.topic, "output_dir": args.output_dir},
            operation="YouTube Shorts generation pipeline"
        )
        return 1



if __name__ == "__main__":
    exit(main())

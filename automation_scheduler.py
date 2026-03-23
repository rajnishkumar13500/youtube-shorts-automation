"""
Automation Scheduler Module.
Orchestrates video generation and upload from Google Sheets.
"""

import logging
import os
import time
import subprocess
from datetime import datetime
from typing import List, Dict

from google_sheets_integration import GoogleSheetsReader
from youtube_uploader import YouTubeUploader
from utils.helpers import setup_logging

logger = setup_logging(module_name="automation_scheduler")


class VideoAutomationScheduler:
    """Automate video generation and upload from Google Sheets."""
    
    def __init__(
        self,
        sheets_credentials: str = None,
        spreadsheet_id: str = None,
        youtube_secrets: str = None,
        output_dir: str = "output"
    ):
        """
        Initialize automation scheduler.
        
        Args:
            sheets_credentials: Path to Google Sheets service account JSON
            spreadsheet_id: Google Sheets spreadsheet ID
            youtube_secrets: Path to YouTube OAuth2 client secrets JSON
            output_dir: Directory for generated videos
        """
        self.output_dir = output_dir
        
        # Initialize Google Sheets reader
        logger.info("Initializing Google Sheets integration")
        self.sheets_reader = GoogleSheetsReader(
            credentials_path=sheets_credentials,
            spreadsheet_id=spreadsheet_id
        )
        
        # Initialize YouTube uploader
        logger.info("Initializing YouTube uploader")
        self.youtube_uploader = YouTubeUploader(
            client_secrets_file=youtube_secrets
        )
        
        logger.info("Automation scheduler initialized successfully")
    
    def process_pending_videos(self, max_videos: int = None, sheet_name: str = "Videos"):
        """
        Process all pending videos from Google Sheets.
        
        Args:
            max_videos: Maximum number of videos to process (None = all)
            sheet_name: Name of the sheet tab
        """
        try:
            logger.info("=" * 80)
            logger.info("Starting video automation process")
            logger.info("=" * 80)
            
            # Read pending videos from Google Sheets
            logger.info("Reading pending videos from Google Sheets")
            video_topics = self.sheets_reader.read_video_topics(sheet_name=sheet_name)
            
            if not video_topics:
                logger.info("No pending videos found")
                return
            
            # Limit number of videos if specified
            if max_videos:
                video_topics = video_topics[:max_videos]
                logger.info(f"Processing first {max_videos} videos")
            
            logger.info(f"Found {len(video_topics)} pending videos to process")
            
            # Process each video
            for i, video_info in enumerate(video_topics, 1):
                logger.info("=" * 80)
                logger.info(f"Processing video {i}/{len(video_topics)}")
                logger.info(f"Topic: {video_info['topic']}")
                logger.info(f"Duration: {video_info['duration']}s")
                logger.info("=" * 80)
                
                try:
                    # Update status to "processing"
                    self.sheets_reader.update_status(
                        row_number=video_info['row_number'],
                        status="processing",
                        sheet_name=sheet_name
                    )
                    
                    # Generate video
                    logger.info("Generating video...")
                    video_path = self._generate_video(
                        topic=video_info['topic'],
                        duration=video_info['duration']
                    )
                    
                    if not video_path or not os.path.exists(video_path):
                        raise RuntimeError("Video generation failed")
                    
                    logger.info(f"Video generated successfully: {video_path}")
                    
                    # Upload to YouTube
                    logger.info("Uploading to YouTube...")
                    upload_result = self._upload_to_youtube(
                        video_path=video_path,
                        topic=video_info['topic']
                    )
                    
                    logger.info(f"Upload successful: {upload_result['video_url']}")
                    
                    # Update status to "completed" with video URL
                    self.sheets_reader.update_status(
                        row_number=video_info['row_number'],
                        status="completed",
                        video_url=upload_result['video_url'],
                        sheet_name=sheet_name
                    )
                    
                    logger.info(f"✓ Video {i}/{len(video_topics)} completed successfully")
                    
                    # Add delay between uploads to avoid rate limits
                    if i < len(video_topics):
                        delay = 10
                        logger.info(f"Waiting {delay} seconds before next video...")
                        time.sleep(delay)
                    
                except Exception as e:
                    logger.error(f"Failed to process video: {e}")
                    
                    # Update status to "failed"
                    try:
                        self.sheets_reader.update_status(
                            row_number=video_info['row_number'],
                            status=f"failed: {str(e)[:100]}",
                            sheet_name=sheet_name
                        )
                    except Exception as update_error:
                        logger.error(f"Failed to update error status: {update_error}")
                    
                    # Continue with next video
                    continue
            
            logger.info("=" * 80)
            logger.info("Video automation process completed")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Automation process failed: {e}")
            raise RuntimeError(f"Automation failed: {e}")
    
    def _generate_video(self, topic: str, duration: int) -> str:
        """
        Generate YouTube Short video.
        
        Args:
            topic: Video topic
            duration: Video duration in seconds
        
        Returns:
            Path to generated video
        """
        try:
            import subprocess
            
            # Call main.py as subprocess
            cmd = [
                "python", "main.py",
                topic,
                "--duration", str(duration),
                "--output-dir", self.output_dir,
                "--verbose"
            ]
            
            logger.info(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Video generation failed: {result.stderr}")
                raise RuntimeError(f"Video generation failed: {result.stderr}")
            
            # Video path is output/final_video_final.mp4
            video_path = os.path.join(self.output_dir, "final_video_final.mp4")
            
            if not os.path.exists(video_path):
                raise RuntimeError(f"Video file not found: {video_path}")
            
            return video_path
            
        except subprocess.TimeoutExpired:
            logger.error("Video generation timeout")
            raise RuntimeError("Video generation timeout (10 minutes)")
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            raise RuntimeError(f"Failed to generate video: {e}")
    
    def _upload_to_youtube(self, video_path: str, topic: str) -> Dict:
        """
        Upload video to YouTube.
        
        Args:
            video_path: Path to video file
            topic: Video topic (used for title)
        
        Returns:
            Upload result dictionary
        """
        try:
            # Generate title and description
            title = self._generate_title(topic)
            description = self._generate_description(topic)
            tags = self._generate_tags(topic)
            
            # Upload video
            result = self.youtube_uploader.upload_video(
                video_path=video_path,
                title=title,
                description=description,
                tags=tags,
                category_id="22",  # People & Blogs
                privacy_status="public",  # Change to "private" or "unlisted" if needed
                made_for_kids=False
            )
            
            return result
            
        except Exception as e:
            logger.error(f"YouTube upload failed: {e}")
            raise RuntimeError(f"Failed to upload to YouTube: {e}")
    
    def _generate_title(self, topic: str) -> str:
        """Generate YouTube video title."""
        # Keep it short and engaging (max 100 chars)
        title = f"{topic} #Shorts"
        return title[:100]
    
    def _generate_description(self, topic: str) -> str:
        """Generate YouTube video description."""
        description = f"""Amazing facts about {topic}!

🔔 Subscribe for more interesting facts and knowledge!
👍 Like if you learned something new!
💬 Comment your thoughts below!

#Shorts #Facts #Knowledge #Learning #Viral #Trending #YouTube
"""
        return description[:5000]
    
    def _generate_tags(self, topic: str) -> List[str]:
        """Generate YouTube video tags."""
        tags = [
            "shorts",
            "facts",
            "knowledge",
            "learning",
            "viral",
            "trending",
            topic.lower()
        ]
        return tags[:15]  # Max 15 tags


def main():
    """Main entry point for automation scheduler."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube Shorts Automation Scheduler")
    parser.add_argument("--sheets-credentials", help="Path to Google Sheets service account JSON")
    parser.add_argument("--spreadsheet-id", help="Google Sheets spreadsheet ID")
    parser.add_argument("--youtube-secrets", help="Path to YouTube OAuth2 client secrets JSON")
    parser.add_argument("--max-videos", type=int, help="Maximum number of videos to process")
    parser.add_argument("--sheet-name", default="Videos", help="Sheet name (default: Videos)")
    parser.add_argument("--output-dir", default="output", help="Output directory")
    
    args = parser.parse_args()
    
    try:
        # Initialize scheduler
        scheduler = VideoAutomationScheduler(
            sheets_credentials=args.sheets_credentials,
            spreadsheet_id=args.spreadsheet_id,
            youtube_secrets=args.youtube_secrets,
            output_dir=args.output_dir
        )
        
        # Process pending videos
        scheduler.process_pending_videos(
            max_videos=args.max_videos,
            sheet_name=args.sheet_name
        )
        
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()

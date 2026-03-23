"""
Schedule 3 Videos Daily - Automated Posting
This script runs continuously and posts 3 videos per day at scheduled times.
"""

import os
import sys
import time
import schedule
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import automation modules
from google_sheets_integration import GoogleSheetsReader
from youtube_uploader import YouTubeUploader
from utils.helpers import setup_logging

logger = setup_logging(module_name="daily_scheduler")


# Configuration
VIDEOS_PER_DAY = 3
POST_TIMES = ["09:00", "15:00", "21:00"]  # 9 AM, 3 PM, 9 PM
VIDEO_DURATION = 20  # 20 seconds


def generate_and_upload_video():
    """Generate one video and upload to YouTube."""
    try:
        logger.info("=" * 80)
        logger.info(f"STARTING VIDEO GENERATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        # Initialize Google Sheets reader
        sheets = GoogleSheetsReader()
        
        # Get pending topics
        topics = sheets.read_video_topics()
        
        if not topics:
            logger.warning("No pending topics found in spreadsheet")
            return False
        
        # Get first pending topic
        topic_data = topics[0]
        topic = topic_data['topic']
        row_number = topic_data['row_number']
        duration = topic_data['duration']
        
        logger.info(f"Topic: {topic}")
        logger.info(f"Duration: {duration} seconds")
        logger.info(f"Row: {row_number}")
        
        # Update status to processing
        sheets.update_status(row_number, "processing")
        
        # Generate video
        logger.info("Generating video...")
        import subprocess
        
        result = subprocess.run(
            ['python', 'main.py', topic, '--duration', str(duration)],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode != 0:
            logger.error(f"Video generation failed: {result.stderr}")
            sheets.update_status(row_number, "failed")
            return False
        
        logger.info("✓ Video generated successfully")
        
        # Upload to YouTube
        logger.info("Uploading to YouTube...")
        
        video_path = "output/final_video_final.mp4"
        
        if not os.path.exists(video_path):
            logger.error(f"Video file not found: {video_path}")
            sheets.update_status(row_number, "failed")
            return False
        
        # Initialize YouTube uploader
        uploader = YouTubeUploader()
        
        # Create title and description
        title = f"{topic.title()} #Shorts"
        description = f"""
{topic.title()}

🔔 Subscribe for daily health & fitness tips!

#Shorts #Health #Fitness #Wellness #HealthTips #FitnessTips
        """.strip()
        
        tags = [
            "shorts",
            "health",
            "fitness",
            "wellness",
            "health tips",
            "fitness tips",
            "healthy lifestyle"
        ]
        
        # Upload video
        upload_result = uploader.upload_video(
            video_path=video_path,
            title=title,
            description=description,
            tags=tags,
            category_id="22",  # People & Blogs
            privacy_status="public"
        )
        
        video_url = upload_result['video_url']
        
        logger.info(f"✓ Video uploaded successfully")
        logger.info(f"✓ URL: {video_url}")
        
        # Update spreadsheet with completed status
        sheets.update_status(row_number, "completed", video_url)
        
        logger.info("=" * 80)
        logger.info("VIDEO COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"Error in video generation/upload: {e}")
        try:
            sheets.update_status(row_number, "failed")
        except:
            pass
        return False


def scheduled_job():
    """Job to run at scheduled times."""
    logger.info(f"Scheduled job triggered at {datetime.now().strftime('%H:%M:%S')}")
    success = generate_and_upload_video()
    
    if success:
        logger.info("✓ Scheduled video posted successfully")
    else:
        logger.error("✗ Scheduled video failed")


def main():
    """Main scheduler loop."""
    print("=" * 80)
    print("DAILY VIDEO SCHEDULER - 3 VIDEOS PER DAY")
    print("=" * 80)
    print()
    print(f"Videos per day: {VIDEOS_PER_DAY}")
    print(f"Post times: {', '.join(POST_TIMES)}")
    print(f"Video duration: {VIDEO_DURATION} seconds")
    print()
    print("Scheduled times:")
    for i, post_time in enumerate(POST_TIMES, 1):
        print(f"  Video {i}: {post_time}")
    print()
    print("=" * 80)
    print()
    
    # Schedule jobs
    for post_time in POST_TIMES:
        schedule.every().day.at(post_time).do(scheduled_job)
        logger.info(f"Scheduled job at {post_time}")
    
    print("Scheduler started. Press Ctrl+C to stop.")
    print()
    
    # Run scheduler loop
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print()
        print("Scheduler stopped by user")
        logger.info("Scheduler stopped by user")


if __name__ == "__main__":
    main()

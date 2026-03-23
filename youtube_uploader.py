"""
YouTube Upload Module.
Uploads videos to YouTube using YouTube Data API v3.
"""

import logging
import os
import time
from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle

from utils.helpers import setup_logging

logger = setup_logging(module_name="youtube_uploader")


class YouTubeUploader:
    """Upload videos to YouTube."""
    
    # YouTube API scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, client_secrets_file: str = None, token_file: str = "youtube_token.pickle"):
        """
        Initialize YouTube uploader.
        
        Args:
            client_secrets_file: Path to OAuth2 client secrets JSON
            token_file: Path to save/load authentication token
        """
        self.client_secrets_file = client_secrets_file or os.getenv('YOUTUBE_CLIENT_SECRETS')
        self.token_file = token_file
        self.service = None
        
        if not self.client_secrets_file:
            raise ValueError("YouTube client secrets file not provided")
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube Data API."""
        try:
            logger.info("Authenticating with YouTube Data API")
            
            creds = None
            
            # Load saved credentials if available
            if os.path.exists(self.token_file):
                logger.info(f"Loading saved credentials from {self.token_file}")
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    logger.info("Refreshing expired credentials")
                    creds.refresh(Request())
                else:
                    logger.info("Getting new credentials via OAuth2 flow")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file, self.SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                
                # Save credentials for future use
                with open(self.token_file, 'wb') as token:
                    pickle.dump(creds, token)
                logger.info(f"Credentials saved to {self.token_file}")
            
            # Build YouTube service
            self.service = build('youtube', 'v3', credentials=creds)
            logger.info("Successfully authenticated with YouTube Data API")
            
        except Exception as e:
            logger.error(f"Failed to authenticate with YouTube: {e}")
            raise RuntimeError(f"YouTube authentication failed: {e}")
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: list = None,
        category_id: str = "22",  # 22 = People & Blogs
        privacy_status: str = "public",  # public, private, unlisted
        made_for_kids: bool = False
    ) -> Dict:
        """
        Upload video to YouTube.
        
        Args:
            video_path: Path to video file
            title: Video title (max 100 characters)
            description: Video description (max 5000 characters)
            tags: List of tags (max 500 characters total)
            category_id: YouTube category ID
            privacy_status: Privacy status (public/private/unlisted)
            made_for_kids: Whether video is made for kids
        
        Returns:
            Dictionary with video ID and URL
        """
        try:
            logger.info(f"Uploading video: {video_path}")
            logger.info(f"Title: {title}")
            logger.info(f"Privacy: {privacy_status}")
            
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title[:100],  # Max 100 characters
                    'description': description[:5000],  # Max 5000 characters
                    'tags': tags or [],
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': made_for_kids
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                video_path,
                mimetype='video/mp4',
                resumable=True,
                chunksize=1024*1024  # 1MB chunks
            )
            
            # Execute upload request
            logger.info("Starting upload to YouTube...")
            request = self.service.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            # Upload with progress tracking
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.info(f"Upload successful!")
            logger.info(f"Video ID: {video_id}")
            logger.info(f"Video URL: {video_url}")
            
            return {
                'video_id': video_id,
                'video_url': video_url,
                'title': title,
                'status': 'uploaded'
            }
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise RuntimeError(f"Failed to upload to YouTube: {e}")
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            raise RuntimeError(f"Failed to upload video: {e}")
    
    def update_video_metadata(
        self,
        video_id: str,
        title: str = None,
        description: str = None,
        tags: list = None
    ):
        """
        Update video metadata after upload.
        
        Args:
            video_id: YouTube video ID
            title: New title (optional)
            description: New description (optional)
            tags: New tags (optional)
        """
        try:
            logger.info(f"Updating metadata for video: {video_id}")
            
            # Get current video details
            video_response = self.service.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                raise ValueError(f"Video not found: {video_id}")
            
            snippet = video_response['items'][0]['snippet']
            
            # Update only provided fields
            if title:
                snippet['title'] = title[:100]
            if description:
                snippet['description'] = description[:5000]
            if tags:
                snippet['tags'] = tags
            
            # Update video
            self.service.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            ).execute()
            
            logger.info(f"Successfully updated video metadata")
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            raise RuntimeError(f"Failed to update video metadata: {e}")
        except Exception as e:
            logger.error(f"Error updating metadata: {e}")
            raise RuntimeError(f"Failed to update metadata: {e}")

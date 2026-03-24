"""
Google Sheets Integration Module.
Reads video topics and configurations from Google Sheets.
"""

import logging
import os
from typing import List, Dict
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.helpers import setup_logging

logger = setup_logging(module_name="google_sheets")


class GoogleSheetsReader:
    """Read video topics from Google Sheets."""
    
    def __init__(self, credentials_path: str = None, spreadsheet_id: str = None):
        """
        Initialize Google Sheets reader.
        
        Args:
            credentials_path: Path to service account JSON credentials
            spreadsheet_id: Google Sheets spreadsheet ID
        """
        self.credentials_path = credentials_path or os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        self.spreadsheet_id = spreadsheet_id or os.getenv('GOOGLE_SHEETS_ID')
        self.service = None
        
        if not self.credentials_path:
            raise ValueError("Google Sheets credentials path not provided")
        
        if not self.spreadsheet_id:
            raise ValueError("Google Sheets spreadsheet ID not provided")
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API."""
        try:
            logger.info("Authenticating with Google Sheets API")
            
            # Use service account credentials
            creds = ServiceAccountCredentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets']  # Full read/write access
            )
            
            self.service = build('sheets', 'v4', credentials=creds)
            logger.info("Successfully authenticated with Google Sheets API")
            
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets: {e}")
            raise RuntimeError(f"Google Sheets authentication failed: {e}")
    
    def read_video_topics(self, sheet_name: str = None, range_name: str = "A2:D") -> List[Dict]:
        """
        Read video topics from Google Sheets.
        
        Expected columns:
        - Column A: Topic
        - Column B: Duration (seconds)
        - Column C: Status (pending/processing/completed/failed)
        - Column D: Video URL (after upload)
        
        Args:
            sheet_name: Name of the sheet tab (if None, uses first sheet)
            range_name: Range to read (default: A2:D to skip header)
        
        Returns:
            List of video topic dictionaries
        """
        try:
            # If no sheet name provided, get the first sheet
            if not sheet_name:
                logger.info("No sheet name provided, finding first sheet")
                spreadsheet = self.service.spreadsheets().get(
                    spreadsheetId=self.spreadsheet_id
                ).execute()
                sheets = spreadsheet.get('sheets', [])
                
                if not sheets:
                    raise RuntimeError("No sheets found in spreadsheet")
                
                sheet_name = sheets[0]['properties']['title']
                logger.info(f"Using first sheet: {sheet_name}")
            
            logger.info(f"Reading video topics from sheet: {sheet_name}")
            
            # Read data from sheet
            range_full = f"{sheet_name}!{range_name}"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_full
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                logger.warning("No data found in Google Sheets")
                return []
            
            # Parse rows into video topic dictionaries
            video_topics = []
            for i, row in enumerate(values, start=2):  # Start at row 2 (after header)
                # Handle incomplete rows
                topic = row[0] if len(row) > 0 else ""
                duration = int(row[1]) if len(row) > 1 and row[1].isdigit() else 30
                status = row[2].lower() if len(row) > 2 else "pending"
                video_url = row[3] if len(row) > 3 else ""
                
                # Only process pending videos
                if status == "pending" and topic.strip():
                    video_topics.append({
                        'row_number': i,
                        'topic': topic.strip(),
                        'duration': duration,
                        'status': status,
                        'video_url': video_url,
                        'sheet_name': sheet_name  # Store sheet name for updates
                    })
                    logger.info(f"Row {i}: Topic='{topic}', Duration={duration}s, Status={status}")
            
            logger.info(f"Found {len(video_topics)} pending video topics")
            return video_topics
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            raise RuntimeError(f"Failed to read from Google Sheets: {e}")
        except Exception as e:
            logger.error(f"Error reading video topics: {e}")
            raise RuntimeError(f"Failed to read video topics: {e}")
    
    def update_status(self, row_number: int, status: str, video_url: str = "", sheet_name: str = None):
        """
        Update video status in Google Sheets.
        
        Args:
            row_number: Row number to update
            status: New status (processing/completed/failed)
            video_url: YouTube video URL (optional)
            sheet_name: Name of the sheet tab (if None, uses first sheet)
        """
        try:
            # If no sheet name provided, get the first sheet
            if not sheet_name:
                logger.info("No sheet name provided, finding first sheet")
                spreadsheet = self.service.spreadsheets().get(
                    spreadsheetId=self.spreadsheet_id
                ).execute()
                sheets = spreadsheet.get('sheets', [])
                
                if not sheets:
                    raise RuntimeError("No sheets found in spreadsheet")
                
                sheet_name = sheets[0]['properties']['title']
                logger.info(f"Using first sheet: {sheet_name}")
            
            logger.info(f"Updating row {row_number}: status={status}, url={video_url}")
            
            # Prepare update data
            values = [[status, video_url]] if video_url else [[status]]
            range_name = f"{sheet_name}!C{row_number}:D{row_number}"
            
            body = {
                'values': values
            }
            
            # Update the sheet
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"Successfully updated row {row_number}")
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            raise RuntimeError(f"Failed to update Google Sheets: {e}")
        except Exception as e:
            logger.error(f"Error updating status: {e}")
            raise RuntimeError(f"Failed to update status: {e}")

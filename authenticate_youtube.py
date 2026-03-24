"""
Authenticate YouTube - Creates youtube_token.pickle
"""

import os
from dotenv import load_dotenv
from youtube_uploader import YouTubeUploader

# Load environment variables
load_dotenv()

print("=" * 80)
print("YOUTUBE AUTHENTICATION")
print("=" * 80)
print()
print("This will open a browser window for YouTube authentication.")
print("Please login with the CORRECT YouTube account.")
print()

try:
    # Get client secrets path from environment
    client_secrets = os.getenv('YOUTUBE_CLIENT_SECRETS')
    
    if not client_secrets:
        print("✗ YOUTUBE_CLIENT_SECRETS not set in .env file")
        exit(1)
    
    if not os.path.exists(client_secrets):
        print(f"✗ Client secrets file not found: {client_secrets}")
        exit(1)
    
    print(f"✓ Using client secrets: {client_secrets}")
    print()
    
    # Initialize uploader (this will trigger authentication)
    uploader = YouTubeUploader(client_secrets_file=client_secrets)
    
    print()
    print("=" * 80)
    print("✓ Authentication successful!")
    print("=" * 80)
    print()
    print("youtube_token.pickle has been created.")
    print()
    print("Next step: Encode the token for GitHub")
    print("Run this command:")
    print()
    print('[Convert]::ToBase64String([IO.File]::ReadAllBytes("youtube_token.pickle")) | Out-File -Encoding ASCII youtube_token_base64.txt')
    print()
    print("Then: Get-Content youtube_token_base64.txt")
    print()
    
except Exception as e:
    print(f"✗ Authentication failed: {e}")
    print()

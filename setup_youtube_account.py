"""
Setup YouTube Account - Reset Authentication
This script will help you authenticate with the correct YouTube account.
"""

import os
import sys

def reset_youtube_auth():
    """Reset YouTube authentication by deleting the token file."""
    print("=" * 80)
    print("YOUTUBE ACCOUNT SETUP")
    print("=" * 80)
    print()
    
    token_file = "youtube_token.pickle"
    
    # Check if token file exists
    if os.path.exists(token_file):
        print(f"✓ Found existing token file: {token_file}")
        print("  This contains authentication for a YouTube account.")
        print()
        
        response = input("Do you want to delete it and re-authenticate? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            try:
                os.remove(token_file)
                print(f"✓ Deleted {token_file}")
                print()
            except Exception as e:
                print(f"✗ Error deleting token file: {e}")
                return False
        else:
            print("Keeping existing authentication.")
            return False
    else:
        print(f"✓ No existing token file found.")
        print()
    
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. Make sure you're logged into the CORRECT YouTube account in your browser")
    print("2. Run the automation script:")
    print("   python automation_scheduler.py")
    print()
    print("3. A browser window will open asking you to:")
    print("   - Choose your Google account")
    print("   - Grant permissions to upload videos")
    print()
    print("4. After granting permissions, the authentication will be saved")
    print("   and future uploads will use this account automatically")
    print()
    print("=" * 80)
    print()
    
    return True


if __name__ == "__main__":
    print()
    reset_youtube_auth()
    print("Setup complete!")
    print()

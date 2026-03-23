# YouTube Shorts Automation - Requirements

## Overview
Build a Python-based automation system that generates YouTube Shorts videos using AI services (OpenAI, ElevenLabs, Stability AI) and FFmpeg for video editing.

## Core Requirements

### 1. Script Generation
- Use OpenAI API to generate 15-second Hinglish scripts
- Include emotional markers: [slow], [pause], [intense]
- Dramatic style with strong hook in first line
- "What happens if" format

### 2. Voice Generation
- Use ElevenLabs API for text-to-speech
- Remove bracket instructions before sending
- Generate MP3 audio saved as output/audio.mp3
- Configurable: voice_id, stability, similarity_boost

### 3. Image Generation (Context-Aware AI)
- Use Groq AI to generate detailed image prompts with FULL CONTEXT
- Pass complete script + topic + current dialogue to AI for each image
- AI generates 50-80 word detailed prompts that match dialogue timing
- Use Cloudflare AI to generate images from AI prompts
- Split script into 4-8 scenes based on audio duration
- Each image must be contextually relevant to its dialogue segment
- Cinematic, photorealistic, dramatic lighting style
- 9:16 vertical aspect ratio (1080x1920)
- Save as output/images/scene_1.png through scene_n.png
- Images must sync perfectly with dialogue timing

### 4. Video Generation (FFmpeg)
- Create vertical video (1080x1920, 9:16)
- Each image duration: based on Whisper-extracted dialogue timing
- Ken Burns zoom-in effect
- Fade transitions between scenes
- CRITICAL: Perfect audio-video sync using cumulative timing
- Images must change EXACTLY when dialogue changes (no lag, no rush)
- Use setpts filter for precise frame-level timing control
- Output: output/final_video.mp4

### 5. Subtitles (Clean & Professional)
- Generate subtitles from script WITHOUT emotional markers
- Remove [whisper], [pause], [intense], etc. from subtitle text
- Remove color codes from subtitle file (apply via FFmpeg)
- Use single professional font (Montserrat Black)
- Bold emphasis on important words only
- Short phrases (max 2 seconds per subtitle)
- Burn subtitles into video using FFmpeg with yellow color
- Subtitles must sync with audio timing

## Bonus Features
- Auto split script into scenes
- Background music (optional)
- Sound effects (whoosh transitions)
- CLI input: topic name
- Batch mode: generate multiple videos

## Project Structure
```
youtube-shorts-automation/
├── main.py (entry point)
├── script_generator.py
├── voice_generator.py
├── image_generator.py
├── video_editor.py
├── config.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
├── output/
│   ├── audio.mp3
│   ├── images/
│   │   ├── scene_1.png
│   │   └── ...
│   └── final_video.mp4
└── requirements.txt
```

## Technical Requirements
- Use Python 3.8+
- Environment variables for API keys
- Clean, modular code with comments
- Error handling throughout
- Logging for each step
- Optimize for speed and low cost

## Output
- Audio file (output/audio.mp3)
- Images (output/images/scene_*.png)
- Final video (output/final_video.mp4)
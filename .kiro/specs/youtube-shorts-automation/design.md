# YouTube Shorts Automation - Design

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py (CLI)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
┌──────────────┐ ┌───────────┐ ┌──────────────┐
│ Script Gen   │ │ Voice     │ │ Image        │
│ (OpenAI)     │ │ (ElevenLabs)│ │ (Stability)│
└──────────────┘ └───────────┘ └──────────────┘
         │             │             │
         └─────────────┼─────────────┘
                       ▼
              ┌───────────────┐
              │ Video Editor  │
              │ (FFmpeg)      │
              └───────────────┘
                       ▼
              ┌───────────────┐
              │ Output        │
              │ (Video +      │
              │ Subtitles)    │
              └───────────────┘
```

## Module Design

### Context-Aware Image Generation Strategy

The key improvement is providing FULL CONTEXT to AI for image generation:

**Problem**: Images were generic and didn't match dialogue content
**Solution**: Pass complete script + topic + current dialogue to Groq AI

**Process**:
1. Split script into 4-8 dialogue segments based on audio duration
2. For EACH segment, call Groq AI with:
   - Full original script (for context)
   - Current dialogue segment (what's being said)
   - Scene number and total scenes
   - Topic information
3. AI generates detailed 50-80 word prompt that:
   - Matches the dialogue content exactly
   - Includes cinematic details (lighting, composition, mood)
   - Specifies 9:16 vertical format
   - Suggests color theme
4. Cloudflare AI generates image from detailed prompt
5. Images are timed to match dialogue duration

**Example**:
- Dialogue: "Kya aap jaante hain agar aap roz 8 glass paani peete hain?"
- Context: Full script about water benefits
- AI Prompt: "Photorealistic close-up of shocked person with wide eyes, hands on cheeks, dramatic lighting, floating holographic water glass glowing cyan, mysterious background, 9:16 vertical, professional photography"
- Result: Image perfectly matches the question being asked

### config.py
- Load environment variables for API keys
- Default configuration values
- Output directory setup

### utils/helpers.py
- Common utility functions
- Logging setup
- File path management
- Error handling helpers

### script_generator.py
- `generate_script(topic: str) -> str`
- Call OpenAI API with prompt
- Parse and return Hinglish script
- Extract emotional markers

### voice_generator.py
- `generate_voice(script: str) -> str`
- Clean script (remove brackets)
- Call ElevenLabs API
- Save audio.mp3
- Return audio path

### image_generator.py
- `generate_ai_image_prompts(script: str, audio_duration: float, topic: str = None) -> list[dict]`
  - Split script into 4-8 dialogue segments
  - For each segment, call Groq AI with FULL CONTEXT:
    - **Original topic** (e.g., "benefits of drinking water")
    - **Complete original script** (full narration for context)
    - **Current dialogue segment** (what's being said right now)
    - **Scene number and total scenes** (for pacing)
  - AI prompt template:
    ```
    Topic: {topic}
    Full Script: {complete_script}
    Current Dialogue: {current_segment}
    Scene: {scene_num}/{total_scenes}
    
    Generate a detailed 50-80 word image prompt that:
    - Visually represents what's being discussed in current dialogue
    - Matches the context from full script
    - Uses cinematic photography style
    - Specifies 9:16 vertical format
    ```
  - AI generates detailed prompt matching dialogue
  - Returns list of {dialogue, prompt, duration, color_theme}
- `generate_images(prompts: list[dict], output_dir: str) -> list[str]`
  - Call Cloudflare AI API for each prompt
  - Fallback through multiple models if needed
  - Save scene images with proper timing metadata
  - Return image paths

### video_editor.py
- `create_video(images: list[str], audio: str) -> str`
  - FFmpeg command generation
  - Ken Burns effect with proper timing
  - Fade transitions between scenes
  - Extend last image to match full audio duration
  - Perfect audio-video synchronization
- `generate_subtitles(script: str, audio_duration: float) -> str`
  - Clean script (remove ALL emotional markers)
  - Split into short phrases (max 2s each)
  - Add bold formatting to important words
  - NO color codes in subtitle text
  - Generate SRT file with proper timing
- `add_subtitles(video: str, subtitles: str, output: str) -> str`
  - Use Montserrat Black font
  - Apply yellow color via FFmpeg
  - Professional styling (outline, shadow)
  - Burn subtitles into video

### main.py
- CLI argument parsing (topic, duration, verbose, etc.)
- Orchestrate pipeline:
  1. Generate script from topic
  2. Generate voice from script
  3. **Pass topic + script to AI prompt generator** (for context)
  4. Generate context-aware images
  5. Create video with perfect timing
  6. Add clean subtitles
- Error handling
- Progress logging

## Data Flow

1. **Input**: Topic string
2. **Script Generation**: Topic → Groq → Hinglish script with markers + Like/Subscribe ending
3. **Voice Generation**: Script → ElevenLabs → audio.mp3
4. **AI Prompt Generation**: Script + Audio Duration → Groq AI → Detailed contextual prompts for each scene
5. **Image Generation**: AI Prompts → Cloudflare AI → scene_*.png (perfectly synced with dialogue)
6. **Video Generation**: Images + Audio → FFmpeg → final_video.mp4 (with perfect timing)
7. **Subtitle Generation**: Clean Script → SRT file (no markers, no color codes)
8. **Subtitle Burning**: Video + SRT → FFmpeg → final_video_with_subtitles.mp4

## Configuration

```python
# Environment Variables
GROQ_API_KEY
ELEVENLABS_API_KEY
CLOUDFLARE_API_TOKEN
CLOUDFLARE_ACCOUNT_ID

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
IMAGE_DURATION = auto  # calculated from audio_duration / num_scenes

# AI Prompt Settings
MIN_SCENES = 4
MAX_SCENES = 8
PROMPT_LENGTH = "50-80 words"
PROMPT_STYLE = "cinematic, photorealistic, dramatic lighting"

# Subtitle Settings
SUBTITLE_FONT = "Montserrat Black"
SUBTITLE_COLOR = "yellow"
SUBTITLE_MAX_DURATION = 2.0  # seconds per phrase
```

## Error Handling

- Try-catch blocks for API calls
- Retry logic for transient failures
- Graceful degradation
- Detailed logging

## Output Structure

```
output/
├── audio.mp3
├── images/
│   ├── scene_1.png
│   ├── scene_2.png
│   └── ...
└── final_video.mp4
```
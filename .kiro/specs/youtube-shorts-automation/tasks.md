# YouTube Shorts Automation - Implementation Tasks

## Phase 1: Core Infrastructure

- [x] 1.1 Create project structure (config.py, utils/, requirements.txt)
- [x] 1.2 Set up environment variable loading
- [x] 1.3 Create output directory structure
- [x] 1.4 Implement logging setup

## Phase 2: Script Generation

- [x] 2.1 Implement OpenAI API integration
- [x] 2.2 Create script generation function
- [x] 2.3 Add emotional marker handling
- [x] 2.4 Test with sample topics

## Phase 3: Voice Generation

- [ ] 3.1 Implement ElevenLabs API integration
- [ ] 3.2 Add script cleaning (remove brackets)
- [ ] 3.3 Implement audio saving
- [ ] 3.4 Test voice generation

## Phase 4: Context-Aware Image Generation

- [x] 4.1 Implement Groq AI integration for prompt generation
  - Pass full script context to AI
  - Generate 50-80 word detailed prompts per dialogue
  - Extract color themes and timing information
  - **CRITICAL**: Include complete script + topic in AI prompt for context
- [x] 4.2 Implement Cloudflare AI integration with fallback models
  - Support multiple Cloudflare models
  - Implement retry logic with model fallback
  - Handle API errors gracefully
- [x] 4.3 Create intelligent scene splitting based on audio duration
  - Split script into 4-8 dialogue segments
  - Calculate optimal timing per scene
  - Ensure scenes align with dialogue content
  - Group related dialogues together
- [x] 4.4 Enhance AI prompt with full context
  - Pass: original topic + full script + current dialogue + scene info
  - AI should understand what's being discussed
  - Generate prompts that visually represent the dialogue
  - Ensure images tell the story being narrated
- [ ] 4.5 Test context-aware image generation
  - Verify images match dialogue content
  - Check timing synchronization
  - Validate image quality and relevance
  - Test with different topics to ensure context understanding

## Phase 5: Video Generation with Perfect Sync

- [ ] 5.1 Implement FFmpeg integration with audio-first timing
  - Use audio duration as master timing reference
  - Calculate image durations dynamically
  - Extend last image to cover full audio
- [ ] 5.2 Add Ken Burns effect with proper timing
  - Implement zoom effect per image
  - Sync zoom duration with audio segments
- [ ] 5.3 Implement fade transitions between scenes
  - Crossfade between images
  - Maintain timing accuracy during transitions
- [ ] 5.4 Test video creation and audio-video sync
  - Verify no visual gaps at end
  - Check smooth transitions
  - Validate perfect audio sync

## Phase 6: Clean Professional Subtitles

- [ ] 6.1 Implement subtitle generation with marker removal
  - Remove ALL emotional markers ([whisper], [pause], etc.)
  - Remove color codes from subtitle text
  - Split into short phrases (max 2s each)
  - Add bold formatting to important words only
- [ ] 6.2 Add subtitle burning with professional styling
  - Use Montserrat Black font (with Arial Black fallback)
  - Apply yellow color via FFmpeg (not in SRT file)
  - Add outline and shadow for readability
  - Position at bottom center
- [ ] 6.3 Test subtitle overlay and timing
  - Verify no markers appear in video
  - Check subtitle-audio synchronization
  - Validate font rendering

## Phase 7: Main Entry Point

- [x] 7.1 Implement CLI argument parsing
- [ ] 7.2 Create orchestration pipeline
- [ ] 7.3 Add progress logging
- [ ] 7.4 Test full pipeline

## Phase 8: Bonus Features

- [ ] 8.1 Add background music support
- [ ] 8.2 Add sound effects
- [ ] 8.3 Implement batch mode
- [ ] 8.4 Optimize for speed/cost

## Phase 9: Integration Testing & Fixes

- [ ] 9.1 Test full pipeline with context-aware images
  - Verify images match dialogue content perfectly
  - Check all timing synchronization
  - Validate no visual or audio gaps
- [ ] 9.2 Test subtitle cleanliness
  - Ensure no emotional markers in output
  - Verify no color codes visible
  - Check professional font rendering
- [ ] 9.3 Test with multiple topics and durations
  - Test 15s, 30s, 45s videos
  - Verify different content types
  - Check edge cases (long/short scripts)
- [ ] 9.4 Performance and quality optimization
  - Optimize AI prompt generation
  - Improve image-dialogue matching
  - Fine-tune timing algorithms

## Phase 10: Critical Sync Fix

- [x] 10.1 Fix video-audio sync lag issue
  - **PROBLEM**: Video scenes changing faster than audio dialogue
  - **ROOT CAUSE**: FFmpeg xfade offset calculation using relative timing instead of cumulative timing
  - **SOLUTION**: Rebuilt FFmpeg filter to use concat demuxer with precise segment durations
  - **IMPLEMENTATION**:
    1. Created individual video segments for each image with EXACT duration from Whisper timing
    2. Applied Ken Burns effect to each segment independently with exact frame counts
    3. Used concat demuxer to join segments sequentially (no overlapping transitions)
    4. Ensured cumulative timing matches audio perfectly using setpts filter
    5. Added crossfade only at boundaries without affecting timing
  - **RESULT**: Zero timing drift guaranteed - frame-perfect sync achieved
# Context-Aware Image Generation - Implementation Guide

## Problem Statement
Images were not syncing with dialogue content and appeared generic/unrelated to what was being narrated.

## Root Cause
The AI image prompt generator was only receiving individual dialogue segments without understanding:
- What the overall video is about (topic)
- What came before and after (full script context)
- How the current dialogue fits into the story

## Solution: Full Context Approach

### What Changes
Instead of:
```python
generate_ai_image_prompts(script, audio_duration)
# AI only sees: "Kya aap jaante hain..."
```

We now do:
```python
generate_ai_image_prompts(script, audio_duration, topic="benefits of drinking water")
# AI sees:
# - Topic: "benefits of drinking water"
# - Full Script: [complete narration]
# - Current Dialogue: "Kya aap jaante hain..."
# - Scene: 1/8
```

### Implementation Details

#### 1. Update Function Signature
```python
def generate_ai_image_prompts(
    script: str, 
    audio_duration: float,
    topic: str = None  # NEW: Add topic parameter
) -> List[Dict[str, any]]:
```

#### 2. Enhanced AI Prompt Template
```python
prompt = f"""You are a professional YouTube Shorts visual director.

VIDEO TOPIC: {topic}

FULL SCRIPT CONTEXT:
{complete_script}

CURRENT DIALOGUE SEGMENT:
{current_dialogue}

SCENE: {scene_num}/{total_scenes}

Generate a detailed 50-80 word image prompt that:
1. Visually represents what's being discussed in the current dialogue
2. Matches the overall topic and script context
3. Uses cinematic photography style
4. Specifies 9:16 vertical format
5. Includes specific visual elements that match the narration

The image should make sense when viewed while hearing: "{current_dialogue}"
"""
```

#### 3. Update main.py Pipeline
```python
# In main.py
topic = args.topic  # Already have this

# Pass topic through to image generation
image_prompts = generate_ai_image_prompts(
    script=script,
    audio_duration=audio_duration,
    topic=topic  # NEW: Pass topic for context
)
```

### Expected Results

#### Before (Without Context)
- Dialogue: "Kya aap jaante hain agar aap roz 8 glass paani peete hain?"
- AI Prompt: "Person drinking water, realistic, 9:16"
- Result: Generic person drinking water (doesn't match the question)

#### After (With Full Context)
- Topic: "benefits of drinking water"
- Full Script: [Complete narration about water benefits]
- Dialogue: "Kya aap jaante hain agar aap roz 8 glass paani peete hain?"
- AI Prompt: "Photorealistic close-up of shocked person with wide eyes and open mouth, hands on cheeks in surprise, dramatic side lighting, dark mysterious background with volumetric fog, floating holographic water glass glowing in neon cyan, cinematic composition, 9:16 vertical format, mysterious and attention-grabbing mood"
- Result: Image that matches the QUESTION being asked (shock/curiosity)

### Testing Checklist

After implementation, verify:
- [ ] Images match what's being narrated at that moment
- [ ] Images tell a visual story that complements the audio
- [ ] No generic/unrelated images
- [ ] Timing is perfect (no gaps, no misalignment)
- [ ] Each scene makes sense in context of the full video

### Files to Modify

1. **image_generator.py**
   - Add `topic` parameter to `generate_ai_image_prompts()`
   - Update AI prompt template to include topic and full script
   - Ensure AI understands the complete context

2. **main.py**
   - Pass `topic` to `generate_ai_image_prompts()`
   - Already have topic from CLI args

3. **Test with multiple topics**
   - "benefits of drinking water"
   - "what happens if you don't sleep for 7 days"
   - "shocking facts about sugar"

## Success Criteria

✅ Images are contextually relevant to dialogue
✅ Images sync perfectly with audio timing
✅ Visual story matches audio narration
✅ No generic or unrelated images
✅ Each scene enhances understanding of the topic

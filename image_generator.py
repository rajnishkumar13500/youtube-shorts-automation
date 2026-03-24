"""
Image Generator Module - AI-Powered Prompts.
Uses Groq AI to generate detailed image prompts synced with script dialogue.
Uses Cloudflare AI to generate images.
"""

import logging
import os
import re
import requests
from typing import List, Dict
from pathlib import Path

from utils.helpers import logger_image_generator
from config import CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN, IMAGE_WIDTH, IMAGE_HEIGHT, GROQ_API_KEY


# ============================================================================
# Groq Client for AI Prompt Generation
# ============================================================================

try:
    from groq import Groq
    groq_client = Groq(api_key=GROQ_API_KEY)
    logger_image_generator.info("Groq client initialized for image prompt generation")
except Exception as e:
    logger_image_generator.error(f"Failed to initialize Groq client: {e}")
    groq_client = None


# ============================================================================
# Cloudflare AI Models
# ============================================================================

CLOUDFLARE_MODELS = [
    "@cf/stabilityai/stable-diffusion-xl-base-1.0",  # Best quality
    "@cf/bytedance/stable-diffusion-xl-lightning",   # Fast alternative
    "@cf/lykon/dreamshaper-8-lcm",                   # Good quality
]


# ============================================================================
# AI-Powered Image Prompt Generation
# ============================================================================

def generate_ai_image_prompts(script: str, audio_duration: float, topic: str = None, sentence_timings: List[Dict] = None) -> List[Dict[str, any]]:
    """
    Use Groq AI to generate detailed, professional image prompts for each dialogue.
    SIMPLIFIED: Uses simple equal-interval timing.
    
    Args:
        script: The full script with dialogue
        audio_duration: Duration of audio in seconds
        topic: The video topic for context (e.g., "benefits of drinking water")
        sentence_timings: DEPRECATED (ignored)
    
    Returns:
        List of dictionaries with 'dialogue', 'prompt', 'duration', 'color_theme', 'start_time', 'end_time'
    """
    logger_image_generator.info("=" * 80)
    logger_image_generator.info("IMAGE PROMPT GENERATION (SIMPLIFIED)")
    logger_image_generator.info("=" * 80)
    
    if not groq_client:
        raise RuntimeError("Groq client not initialized")
    
    # Clean script
    clean_script = re.sub(r'\[(slow|pause|intense|excited|calm|whisper)\]', '', script)
    clean_script = clean_script.strip('"\'')
    
    # SIMPLIFIED: Use simple sentence splitting
    logger_image_generator.info("Using simple equal-interval timing")
    dialogues = re.split(r'(?<=[.!?])\s+', clean_script)
    dialogues = [d.strip() for d in dialogues if d.strip()]
    
    logger_image_generator.info(f"Creating {len(dialogues)} scenes from dialogue segments")
    
    # Calculate timing for each dialogue based on word count
    total_words = sum(len(d.split()) for d in dialogues)
    words_per_second = total_words / audio_duration if audio_duration > 0 else 3.0
    
    logger_image_generator.info(f"Total words: {total_words}, Words per second: {words_per_second:.2f}")
    
    # Calculate start and end time for each dialogue
    current_time = 0.0
    dialogue_timings = []
    
    for dialogue in dialogues:
        word_count = len(dialogue.split())
        duration = word_count / words_per_second
        start_time = current_time
        end_time = min(current_time + duration, audio_duration)
        
        dialogue_timings.append({
            'text': dialogue,
            'start': start_time,
            'end': end_time,
            'duration': end_time - start_time
        })
        
        current_time = end_time
    
    logger_image_generator.info(f"Video topic: {topic if topic else 'Not specified'}")
    
    # Log timing information
    for i, timing in enumerate(dialogue_timings):
        logger_image_generator.info(
            f"Scene {i+1}: {timing['start']:.2f}s - {timing['end']:.2f}s "
            f"({timing['duration']:.2f}s) | {timing['text'][:50]}..."
        )
    
    # Build prompt for Groq with FULL CONTEXT
    topic_context = f"\n\nVIDEO TOPIC: {topic}" if topic else ""
    
    # Extract dialogue text from timings
    dialogues_text = [t.get('text', t.get('dialogue', '')) for t in dialogue_timings]
    
    prompt = f"""You are a professional YouTube Shorts visual director specializing in ultra-realistic, cinematic photography. Generate HIGHLY DETAILED, photorealistic image prompts for each dialogue segment.
{topic_context}

FULL SCRIPT CONTEXT (for understanding the complete story):
{clean_script}

DIALOGUE SEGMENTS TO VISUALIZE:
{chr(10).join([f"{i+1}. {d}" for i, d in enumerate(dialogues_text)])}

For EACH dialogue above, create an ULTRA-DETAILED photorealistic image prompt following this format:

DIALOGUE 1: [repeat the dialogue]
IMAGE PROMPT: [Ultra-detailed photorealistic description - 80-120 words]
- PHOTOREALISTIC style, professional photography, cinematic quality
- Detailed description of main subject/scene
- Specific background details and environment
- Thematic elements matching the topic (water theme for hydration, medical theme for health, fitness theme for exercise, etc.)
- Lighting: natural light, studio lighting, golden hour, dramatic shadows, etc.
- Camera angle and composition
- Color palette and mood
- Textures and materials
- 9:16 vertical format optimized for mobile viewing
- 8K quality, ultra-sharp, professional photography
- MUST visually represent what's being discussed in this specific dialogue
COLOR THEME: [dominant color scheme - e.g., "cool blue water tones", "warm golden medical", "vibrant green fitness"]

CRITICAL REQUIREMENTS:
1. ULTRA-REALISTIC PHOTOGRAPHIC STYLE - no cartoons, no 3D animation, no illustrations
2. Each prompt must be EXTREMELY DETAILED (80-120 words minimum)
3. Include: main subject, background details, thematic elements, lighting, camera angle, textures, colors, mood
4. Use photography terms: "shallow depth of field", "bokeh", "natural lighting", "macro shot", "wide angle", "golden hour"
5. Match theme to topic:
   - Water/hydration topics: water droplets, glasses of water, blue aquatic backgrounds, fresh clean aesthetic
   - Health/medical topics: medical imagery, clean clinical backgrounds, health symbols, professional medical aesthetic
   - Fitness/exercise topics: gym equipment, active poses, energetic backgrounds, athletic aesthetic
   - Food/nutrition topics: fresh ingredients, healthy meals, vibrant food photography
   - Mental health topics: calm serene environments, peaceful nature, meditation spaces
6. Specify 9:16 vertical format for mobile
7. Match visual to dialogue content - image should enhance the message
8. Choose realistic color palettes that look professional
9. Make it look like a professional magazine or documentary photograph
10. Consider the full script context - images should tell a cohesive visual story

EXAMPLE (for topic "benefits of drinking water"):
DIALOGUE 1: Kya aap jaante hain agar aap roz 8 glass paani peete hain toh kya hoga?
IMAGE PROMPT: Ultra-realistic close-up photograph of a crystal-clear glass of pure water with condensation droplets on the outside, placed on a clean white marble countertop, soft natural window light from the left creating subtle reflections and highlights on the water surface, background shows a blurred modern kitchen with hints of fresh fruits and greenery, water droplets suspended in mid-air around the glass creating a dynamic splash effect, cool blue and cyan color palette with white highlights, shallow depth of field with bokeh effect, professional product photography style, 8K ultra-sharp detail showing every water droplet and reflection, 9:16 vertical mobile format, fresh clean healthy aesthetic, cinematic composition
COLOR THEME: cool blue water tones with white highlights

Now generate ultra-realistic photographic prompts for all {len(dialogue_timings)} dialogues:"""

    try:
        logger_image_generator.info("Sending prompt to Groq AI...")
        logger_image_generator.info(f"Prompt length: {len(prompt)} characters")
        
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert visual director for YouTube Shorts specializing in ultra-realistic, cinematic photography. Create HIGHLY DETAILED photorealistic image prompts that perfectly match dialogue content AND the overall video topic. Use the full script context to understand the story. Be EXTREMELY specific about: main subject details, background elements, thematic elements (water theme for hydration, medical theme for health, etc.), lighting setup, camera angle, textures, materials, color palette, and mood. Each image should look like a professional magazine photograph or documentary shot - ultra-realistic, 8K quality, cinematic composition. NO cartoons, NO 3D animation, NO illustrations - only photorealistic imagery. Make it mobile-optimized (9:16) and visually stunning."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = response.choices[0].message.content
        logger_image_generator.info("AI response received successfully")
        logger_image_generator.info(f"AI response length: {len(ai_response)} characters")
        
        # Log the generated prompts
        logger_image_generator.info("GENERATED IMAGE PROMPTS:")
        logger_image_generator.info("-" * 40)
        
        # Parse the AI response with timing information
        image_prompts = parse_ai_prompts_with_timing(ai_response, dialogue_timings)
        
        # Log each generated prompt
        for i, prompt_info in enumerate(image_prompts):
            logger_image_generator.info(f"Prompt {i+1}:")
            logger_image_generator.info(f"  Dialogue: {prompt_info.get('dialogue', prompt_info.get('text', 'N/A'))[:80]}...")
            logger_image_generator.info(f"  Prompt: {prompt_info.get('prompt', 'N/A')[:100]}...")
            logger_image_generator.info(f"  Color Theme: {prompt_info.get('color_theme', 'N/A')}")
            logger_image_generator.info(f"  Timing: {prompt_info.get('start_time', 0):.2f}s - {prompt_info.get('end_time', 0):.2f}s")
        
        logger_image_generator.info("-" * 40)
        logger_image_generator.info(f"Total prompts generated: {len(image_prompts)}")
        logger_image_generator.info("=" * 80)
        
        return image_prompts
        
    except Exception as e:
        logger_image_generator.error(f"Failed to generate AI prompts: {e}")
        # Fallback to simple prompts with timing
        fallback_prompts = generate_fallback_prompts_with_timing(dialogue_timings)
        logger_image_generator.info(f"Fallback prompts generated: {len(fallback_prompts)}")
        return fallback_prompts


def parse_ai_prompts_with_timing(ai_response: str, dialogue_timings: List[Dict]) -> List[Dict[str, any]]:
    """
    Parse AI-generated prompts into structured format WITH TIMING.
    
    Args:
        ai_response: Raw AI response text
        dialogue_timings: List of dialogue timing dictionaries
    
    Returns:
        List of prompt dictionaries with timing
    """
    logger_image_generator.info("=" * 80)
    logger_image_generator.info("PARSING AI RESPONSE")
    logger_image_generator.info("=" * 80)
    
    prompts = []
    
    # Split by dialogue markers
    sections = re.split(r'DIALOGUE \d+:', ai_response)
    sections = [s.strip() for s in sections if s.strip()]
    
    for i, section in enumerate(sections[:len(dialogue_timings)]):
        timing = dialogue_timings[i]
        
        # Get dialogue text (support both 'text' from Whisper and 'dialogue' from fallback)
        dialogue_text = timing.get('text', timing.get('dialogue', ''))
        
        # Extract image prompt
        prompt_match = re.search(r'IMAGE PROMPT:\s*(.+?)(?=COLOR THEME:|$)', section, re.DOTALL)
        image_prompt = prompt_match.group(1).strip() if prompt_match else dialogue_text
        
        # Extract color theme
        color_match = re.search(r'COLOR THEME:\s*(.+?)(?=\n|$)', section)
        color_theme = color_match.group(1).strip() if color_match else "golden yellow"
        
        logger_image_generator.info(f"Scene {i+1}/{len(dialogue_timings)}:")
        logger_image_generator.info(f"  Timing: {timing['start']:.2f}s - {timing['end']:.2f}s ({timing['duration']:.2f}s)")
        logger_image_generator.info(f"  Dialogue: {dialogue_text[:80]}...")
        logger_image_generator.info(f"  Image Prompt: {image_prompt[:150]}...")
        logger_image_generator.info(f"  Color Theme: {color_theme}")
        
        prompts.append({
            'dialogue': dialogue_text,
            'prompt': image_prompt,
            'start_time': timing['start'],
            'end_time': timing['end'],
            'duration': timing['duration'],
            'color_theme': color_theme,
            'scene_number': i + 1
        })
    
    # Fill in any missing prompts
    while len(prompts) < len(dialogue_timings):
        i = len(prompts)
        timing = dialogue_timings[i]
        dialogue_text = timing.get('text', timing.get('dialogue', ''))
        
        logger_image_generator.warning(f"Missing prompt for scene {i+1}, using fallback")
        
        prompts.append({
            'dialogue': dialogue_text,
            'prompt': f"Ultra-realistic photorealistic scene: {dialogue_text}, professional photography, cinematic lighting, 8K quality, natural colors, 9:16 vertical format",
            'start_time': timing['start'],
            'end_time': timing['end'],
            'duration': timing['duration'],
            'color_theme': "natural realistic tones",
            'scene_number': i + 1
        })
    
    logger_image_generator.info(f"Parsed {len(prompts)} AI-generated prompts with timing")
    logger_image_generator.info("=" * 80)
    
    return prompts


def generate_fallback_prompts_with_timing(dialogue_timings: List[Dict]) -> List[Dict[str, any]]:
    """
    Generate simple fallback prompts with timing if AI generation fails.
    
    Args:
        dialogue_timings: List of dialogue timing dictionaries
    
    Returns:
        List of prompt dictionaries with timing
    """
    logger_image_generator.warning("=" * 80)
    logger_image_generator.warning("FALLBACK PROMPT GENERATION")
    logger_image_generator.warning("=" * 80)
    logger_image_generator.warning(f"Generating {len(dialogue_timings)} fallback prompts")
    
    prompts = []
    
    for i, timing in enumerate(dialogue_timings):
        # Get dialogue text (support both 'text' from Whisper and 'dialogue' from fallback)
        dialogue_text = timing.get('text', timing.get('dialogue', ''))
        
        prompt = f"Ultra-realistic photorealistic scene: {dialogue_text}, professional photography, cinematic lighting, 8K quality, sharp details, natural colors, 9:16 vertical format, magazine quality"
        
        logger_image_generator.warning(f"Prompt {i+1}:")
        logger_image_generator.warning(f"  Dialogue: {dialogue_text[:80]}...")
        logger_image_generator.warning(f"  Prompt: {prompt[:100]}...")
        logger_image_generator.warning(f"  Timing: {timing['start']:.2f}s - {timing['end']:.2f}s")
        
        prompts.append({
            'dialogue': dialogue_text,
            'prompt': prompt,
            'start_time': timing['start'],
            'end_time': timing['end'],
            'duration': timing['duration'],
            'color_theme': "golden yellow",
            'scene_number': i + 1
        })
    
    logger_image_generator.warning(f"Fallback prompts generated: {len(prompts)}")
    logger_image_generator.warning("=" * 80)
    
    return prompts


def parse_ai_prompts(ai_response: str, dialogues: List[str], audio_duration: float) -> List[Dict[str, any]]:
    """
    Parse AI-generated prompts into structured format.
    
    Args:
        ai_response: Raw AI response text
        dialogues: List of dialogue segments
        audio_duration: Total audio duration
    
    Returns:
        List of prompt dictionaries
    """
    prompts = []
    duration_per_scene = audio_duration / len(dialogues)
    
    # Split by dialogue markers
    sections = re.split(r'DIALOGUE \d+:', ai_response)
    sections = [s.strip() for s in sections if s.strip()]
    
    for i, section in enumerate(sections[:len(dialogues)]):
        # Extract image prompt
        prompt_match = re.search(r'IMAGE PROMPT:\s*(.+?)(?=COLOR THEME:|$)', section, re.DOTALL)
        image_prompt = prompt_match.group(1).strip() if prompt_match else dialogues[i]
        
        # Extract color theme
        color_match = re.search(r'COLOR THEME:\s*(.+?)(?=\n|$)', section)
        color_theme = color_match.group(1).strip() if color_match else "natural realistic tones"
        
        # LOG THE FULL PROMPT FOR DEBUGGING
        logger_image_generator.info(f"=" * 80)
        logger_image_generator.info(f"SCENE {i+1}/{len(dialogues)}")
        logger_image_generator.info(f"Dialogue: {dialogues[i][:100]}...")
        logger_image_generator.info(f"AI Generated Prompt: {image_prompt}")
        logger_image_generator.info(f"Color Theme: {color_theme}")
        logger_image_generator.info(f"=" * 80)
        
        prompts.append({
            'dialogue': dialogues[i],
            'prompt': image_prompt,
            'duration': duration_per_scene,
            'color_theme': color_theme,
            'scene_number': i + 1
        })
    
    # Fill in any missing prompts
    while len(prompts) < len(dialogues):
        i = len(prompts)
        prompts.append({
            'dialogue': dialogues[i],
            'prompt': f"Ultra-realistic photorealistic scene: {dialogues[i]}, professional photography, cinematic lighting, 8K quality, natural colors, 9:16 vertical format",
            'duration': duration_per_scene,
            'color_theme': "natural realistic tones",
            'scene_number': i + 1
        })
    
    logger_image_generator.info(f"Parsed {len(prompts)} AI-generated prompts")
    return prompts


def generate_fallback_prompts(dialogues: List[str], audio_duration: float) -> List[Dict[str, any]]:
    """
    Generate simple fallback prompts if AI generation fails.
    
    Args:
        dialogues: List of dialogue segments
        audio_duration: Total audio duration
    
    Returns:
        List of prompt dictionaries
    """
    logger_image_generator.warning("Using fallback prompts")
    
    prompts = []
    duration_per_scene = audio_duration / len(dialogues)
    
    for i, dialogue in enumerate(dialogues):
        prompts.append({
            'dialogue': dialogue,
            'prompt': f"Professional cinematic scene: {dialogue}, photorealistic, dramatic lighting, high detail, 9:16 vertical format, professional photography",
            'duration': duration_per_scene,
            'color_theme': "golden yellow",
            'scene_number': i + 1
        })
    
    return prompts


# ============================================================================
# Image Generation with Cloudflare AI
# ============================================================================

def generate_single_image(
    prompt: str,
    output_path: str,
    account_id: str,
    api_token: str
) -> str:
    """
    Generate a single image with fallback support.
    
    Args:
        prompt: Detailed image prompt
        output_path: Path to save image
        account_id: Cloudflare account ID
        api_token: Cloudflare API token
    
    Returns:
        Path to generated image or None
    """
    logger_image_generator.info("=" * 80)
    logger_image_generator.info("IMAGE GENERATION LOG")
    logger_image_generator.info("=" * 80)
    logger_image_generator.info(f"Output path: {output_path}")
    logger_image_generator.info(f"Prompt: {prompt[:150]}...")
    
    for model in CLOUDFLARE_MODELS:
        logger_image_generator.info(f"Attempting with {model}")
        
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
        
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {"prompt": prompt}
        
        if "xl" in model.lower():
            payload["num_steps"] = 20
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                image_data = response.content
                
                if image_data and len(image_data) > 100:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    logger_image_generator.info(f"✓ Image saved: {output_path}")
                    logger_image_generator.info("=" * 80)
                    return output_path
            else:
                logger_image_generator.warning(f"✗ Failed with {model}: {response.status_code}")
                
        except Exception as e:
            logger_image_generator.warning(f"✗ Error with {model}: {e}")
            continue
    
    logger_image_generator.error(f"All models failed for prompt")
    logger_image_generator.error("=" * 80)
    return None


def generate_images(prompts: List[Dict[str, any]], output_dir: str) -> List[str]:
    """
    Generate images from AI-generated prompts.
    
    Args:
        prompts: List of prompt dictionaries
        output_dir: Directory to save images
    
    Returns:
        List of image paths
    """
    logger_image_generator.info("=" * 80)
    logger_image_generator.info("IMAGE GENERATION PROGRESS")
    logger_image_generator.info("=" * 80)
    logger_image_generator.info(f"Output directory: {output_dir}")
    logger_image_generator.info(f"Total images to generate: {len(prompts)}")
    
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        raise RuntimeError("Cloudflare credentials not configured")
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    image_paths = []
    
    for prompt_data in prompts:
        scene_num = prompt_data['scene_number']
        prompt = prompt_data['prompt']
        output_path = os.path.join(output_dir, f"scene_{scene_num}.png")
        
        logger_image_generator.info("-" * 40)
        logger_image_generator.info(f"Generating image {scene_num}/{len(prompts)}")
        logger_image_generator.info(f"Prompt: {prompt[:150]}...")
        
        result = generate_single_image(
            prompt=prompt,
            output_path=output_path,
            account_id=CLOUDFLARE_ACCOUNT_ID,
            api_token=CLOUDFLARE_API_TOKEN
        )
        
        if result:
            image_paths.append(result)
            logger_image_generator.info(f"✓ Image {scene_num} generated successfully")
        else:
            logger_image_generator.error(f"✗ Failed to generate image {scene_num}")
    
    logger_image_generator.info("-" * 40)
    logger_image_generator.info(f"Generated {len(image_paths)}/{len(prompts)} images successfully")
    logger_image_generator.info("=" * 80)
    
    if len(image_paths) == 0:
        raise RuntimeError("Failed to generate any images")
    
    return image_paths

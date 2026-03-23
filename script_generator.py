"""
Script Generator Module.
Uses Groq API to generate Hinglish scripts with emotional markers.
"""

import logging

from utils.helpers import logger_script_generator
from config import GROQ_API_KEY


# ============================================================================
# Groq Client Setup
# ============================================================================

try:
    from groq import Groq

    groq_client = Groq(api_key=GROQ_API_KEY)
    logger_script_generator.info("Groq client initialized successfully")
except Exception as e:
    logger_script_generator.error(f"Failed to initialize Groq client: {e}")
    groq_client = None


# ============================================================================
# Script Generation
# ============================================================================

def generate_script(topic: str, duration: int = 30, model: str = None) -> str:
    """
    Generate an impactful YouTube Shorts script using Groq API.

    Args:
        topic: The topic for the script (e.g., "not eating for 7 days")
        duration: Target duration in seconds (15-45, default: 30)
        model: Groq model to use (default: openai/gpt-oss-120b from config, alternatives: llama-3.3-70b-versatile, mixtral-8x7b-32768)

    Returns:
        Generated script with emotional markers

    Raises:
        RuntimeError: If Groq API call fails
    """
    logger_script_generator.info("=" * 80)
    logger_script_generator.info("SCRIPT GENERATION LOG")
    logger_script_generator.info("=" * 80)
    logger_script_generator.info(f"Generating script for topic: {topic}")
    logger_script_generator.info(f"Target duration: {duration} seconds")
    
    # Use default model from config if none provided
    if model is None:
        from config import DEFAULT_GROQ_MODEL
        model = DEFAULT_GROQ_MODEL
        logger_script_generator.info(f"Using default model from config: {model}")
    else:
        logger_script_generator.info(f"Using Groq model: {model}")

    if not groq_client:
        error_msg = "Groq client not initialized. Check API key configuration."
        logger_script_generator.error(error_msg)
        raise RuntimeError(error_msg)

    # Calculate word count based on duration (fast pace: 3 words per second)
    # Be more conservative to avoid exceeding duration
    word_count = int(duration * 2.8)  # Slightly slower to ensure we don't exceed
    min_word_count = int(duration * 2.5)
    max_word_count = int(duration * 3.2)  # Hard limit

    logger_script_generator.info(f"Word count range: {min_word_count} - {max_word_count} words (target: {word_count})")

    # Build the prompt for impactful shorts with STRONG HOOK
    prompt = f"""Create a {duration}-second YouTube Shorts script in Hinglish (Hindi + English mix) about: "{topic}"

CRITICAL REQUIREMENTS FOR VIRAL CONTENT:

1. HOOK (First 3 seconds - MOST IMPORTANT):
   - Start with a SHOCKING question or statement
   - Use "Kya aap jaante hain..." or "Yeh sunke aap shocked ho jayenge..."
   - Create CURIOSITY and SUSPENSE
   - Make viewers think "I NEED to know this!"
   
2. STRUCTURE:
   - Hook (0-3s): Shocking question/statement
   - Problem/Setup (3-8s): Why this matters
   - Revelation (8-20s): The surprising facts (use numbers, days, specific details)
   - Payoff (20s-end): The result, transformation, or call-to-action
   
3. PACING:
   - FAST delivery: 3-4 words per second
   - Short sentences: Maximum 8-10 words each
   - Use numbers and specific details: "Day 1", "3 hours", "80% improvement"
   - Build suspense: Don't reveal everything at once
   
4. EMOTIONAL MARKERS:
   - [pause] - After hook or before big reveal
   - [intense] - For shocking facts
   - [excited] - For positive results
   - [whisper] - For secrets or insider info
   
5. WORD COUNT (STRICT):
   - MINIMUM {min_word_count} words
   - TARGET {word_count} words  
   - MAXIMUM {max_word_count} words (DO NOT EXCEED!)
   - Keep it concise and fast-paced
   - If you exceed {max_word_count} words, the script will be TOO LONG
   
6. LANGUAGE:
   - Simple Hinglish (70% Hindi, 30% English)
   - Use relatable words: "aap", "kya", "jaante hain", "shocking"
   - Mix English for impact words: "shocking", "amazing", "transform"

VIRAL SCRIPT FORMULA:

Hook Examples:
- "Kya aap jaante hain agar aap 7 din tak sugar na khaayein toh kya hoga? [pause]"
- "Yeh sunke aap shocked ho jayenge! [pause] Agar aap subah khali pet paani peete hain..."
- "Doctors yeh baat chhupate hain! [whisper] Agar aap..."

Body Structure:
- Use "Day 1:", "Day 3:", "Day 7:" for progression
- Use "Pehle din:", "Teesre din:", "Satve din:" in Hindi
- Include specific numbers: "80% log", "3 ghante mein", "5 din baad"
- Build tension: "Aur ab sabse badi baat..." [pause]

Ending:
- Strong call-to-action: "Toh aaj se hi shuru karein!"
- Create urgency: "Abhi try karein!"
- Leave impact: "Aapki zindagi badal jayegi!"

EXAMPLE VIRAL SCRIPT (30 seconds):
"Kya aap jaante hain agar aap 7 din tak sugar bilkul band kar dein toh kya hoga? [pause] Yeh sunke aap shocked ho jayenge! [intense] Pehle din: Aapka body fat burn karna shuru kar dega. Cravings badhenge, par yeh normal hai! [pause] Teesre din tak: Energy levels 80% badh jayenge! Aap zyada alert mehsoos karenge. [excited] Paanchve din: Twacha bilkul saaf ho jayegi! Inflammation 50% kam hoga! [intense] Satve din: Wazan 2-3 kg kam, mood behtar, neend acchi! [pause] Aur sabse badi baat... aapki body ab sugar ke bina kaam kar sakti hai! [excited] Toh aaj se hi sugar chhodein aur apne aapko transform karein! Yeh 7 din aapki zindagi badal denge! [pause] Agar aapko yeh video pasand aaya toh like karein aur channel ko subscribe zaroor karein!"

IMPORTANT ENDING:
- ALWAYS end with: "Agar aapko yeh video pasand aaya toh like karein aur channel ko subscribe zaroor karein!"
- OR: "Video pasand aayi? Like aur subscribe karein!"
- OR: "Like karein, subscribe karein, aur bell icon dabayein!"

Now create a VIRAL script with a STRONG HOOK for: "{topic}"
MINIMUM {min_word_count} words, make it ATTENTION-GRABBING and END with like/subscribe call:"""

    try:
        logger_script_generator.info("Sending prompt to Groq API...")
        logger_script_generator.info(f"Prompt length: {len(prompt)} characters")
        
        # Check if using GPT OSS model (requires OpenAI client format)
        if model and "gpt-oss" in model.lower():
            logger_script_generator.info(f"Using GPT OSS model: {model}")
            # GPT OSS model uses OpenAI-compatible API format
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert YouTube Shorts scriptwriter specializing in viral health and science content. Create FAST-PACED, IMPACTFUL scripts that grab attention immediately. Use Hinglish naturally. Keep energy HIGH throughout."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,  # Higher for more creative, energetic output
                max_tokens=1000  # Increased for GPT OSS model
            )
        else:
            # Standard Groq models
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert YouTube Shorts scriptwriter specializing in viral health and science content. Create FAST-PACED, IMPACTFUL scripts that grab attention immediately. Use Hinglish naturally. Keep energy HIGH throughout."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.9,  # Higher for more creative, energetic output
                max_tokens=1000  # Increased for better responses
            )

        raw_script = response.choices[0].message.content.strip()
        logger_script_generator.info(f"Raw script response: {raw_script[:500]}...")
        
        # Clean up the script - remove markdown code blocks if present
        import re
        if raw_script.startswith("```") and "```" in raw_script[3:]:
            # Extract content between markdown code blocks
            match = re.search(r'```(?:hinglish|python)?\s*(.*?)\s*```', raw_script, re.DOTALL)
            if match:
                script = match.group(1).strip()
                logger_script_generator.info(f"Extracted script from markdown: {script[:200]}...")
            else:
                script = raw_script
        else:
            script = raw_script
        
        logger_script_generator.info("✓ Script generated successfully via Groq API")
        logger_script_generator.info(f"Script length: {len(script.split())} words")
        logger_script_generator.info(f"Script: {script[:200]}...")
        
        # Check if script has emotional markers, if not add them
        if not re.search(r'\[(slow|pause|intense|excited|calm|whisper)\]', script):
            logger_script_generator.warning("No emotional markers found in generated script. Adding default markers.")
            # Add default markers at key points
            script = script.replace("Yeh sunke aap shocked ho jayenge!", "Yeh sunke aap shocked ho jayenge! [pause]")
            script = script.replace("Pehle din:", "Pehle din: [pause]")
            script = script.replace("Teesre din:", "Teesre din: [pause]")
            script = script.replace("Paanchve din:", "Paanchve din: [pause]")
            script = script.replace("Aur sabse badi baat", "Aur sabse badi baat... [pause]")
            logger_script_generator.info(f"Script with added markers: {script[:200]}...")
        
        logger_script_generator.info("=" * 80)
        return script

    except Exception as e:
        logger_script_generator.error(f"Groq API call failed: {e}")
        raise RuntimeError(f"Failed to generate script: {e}")


def clean_script(script: str) -> str:
    """
    Remove emotional markers from script for voice generation.

    Args:
        script: Script with emotional markers

    Returns:
        Cleaned script without markers
    """
    import re

    # Remove markers like [slow], [pause], [intense]
    cleaned = re.sub(r'\[(slow|pause|intense|excited|calm)\]', '', script)
    return cleaned.strip()


def extract_emotional_markers(script: str) -> list:
    """
    Extract emotional markers from script.

    Args:
        script: Script with emotional markers

    Returns:
        List of (marker, position) tuples
    """
    import re

    pattern = r'\[(slow|pause|intense|excited|calm|whisper)\]'
    markers = []

    for match in re.finditer(pattern, script):
        markers.append({
            'marker': match.group(1),
            'position': match.start(),
            'text': match.group(0)
        })

    return markers

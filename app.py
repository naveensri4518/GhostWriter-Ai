"""
GhostWriter AI - Stories from the Other Side
Flask Backend with Local Ollama AI Integration
Built for Hacktoberfest Open-Source AI Challenge Week 4: 'Ghost in the Machine'
"""

import os
import re
import sys
import time
import logging

# Ensure UTF-8 stream handling on Windows
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from flask import Flask, render_template, request, jsonify
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ghostwriter")

# Application paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

# Configuration from environment variables
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "120"))

# Valid category and ending options
VALID_CATEGORIES = [
    "Haunted House",
    "Supernatural",
    "Psychological Horror",
    "Ghost Stories",
    "Urban Legends"
]

VALID_ENDINGS = [
    "Terrifying",
    "Tragic",
    "Unexpected Twist"
]

CATEGORY_TONE_MAP = {
    "Haunted House": (
        "Focus on oppressive architectural isolation, creaking timbers, "
        "rooms that feel watchful, shifting shadows, and historic curses trapped within rotting walls."
    ),
    "Supernatural": (
        "Focus on otherworldly entities that defy physical laws, ancient rituals, "
        "eldritch dread, cold spots, spectral anomalies, and malevolent occult forces."
    ),
    "Psychological Horror": (
        "Focus on mounting paranoia, distorted perception of reality, auditory hallucinations, "
        "unreliable memories, claustrophobia, and the terrifying descent into madness."
    ),
    "Ghost Stories": (
        "Focus on lingering restless spirits, unfinished earthly business, tragic apparitions, "
        "whispering specters, midnight hauntings, and chilling cold drafts."
    ),
    "Urban Legends": (
        "Focus on eerie modern folklore, forbidden nighttime rituals, forgotten city corridors, "
        "cursed technology or relics, and ominous warnings whispered by locals."
    )
}

ENDING_INSTRUCTION_MAP = {
    "Terrifying": (
        "The story MUST culminate in an overwhelmingly terrifying, inescapable climax. "
        "Deliver pure dread, impending doom, or an unresolved horror that lingers in the dark."
    ),
    "Tragic": (
        "The story MUST culminate in a heartbreaking, sorrowful conclusion. "
        "Unveil an emotional loss, a poignant sacrifice, or an agonizing curse that leaves the reader sorrowful."
    ),
    "Unexpected Twist": (
        "The story MUST culminate in a mind-bending, shocking plot twist. "
        "Subvert the reader's assumptions completely, inverting the reality of who or what the true horror is."
    )
}


def fetch_available_models():
    """Queries Ollama for currently installed local models."""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=4)
        if response.status_code == 200:
            data = response.json()
            models = [m.get("name") for m in data.get("models", []) if m.get("name")]
            return True, models
        return False, []
    except Exception as e:
        logger.warning(f"Failed to query Ollama models: {e}")
        return False, []


def is_model_installed(target_model, available_models):
    """
    Checks if target_model is installed, matching exact or base name (e.g. 'qwen2.5:3b' or 'qwen2.5:3b:latest').
    """
    if not target_model or not available_models:
        return False
    target_clean = target_model.strip().lower()
    for m in available_models:
        m_clean = m.strip().lower()
        if m_clean == target_clean:
            return True
        # Match 'qwen2.5:3b' with 'qwen2.5:3b:latest' or vice-versa
        if m_clean.split(":")[0] == target_clean.split(":")[0]:
            target_tag = target_clean.split(":")[1] if ":" in target_clean else "latest"
            m_tag = m_clean.split(":")[1] if ":" in m_clean else "latest"
            if target_tag == m_tag or target_tag == "latest" or m_tag == "latest":
                return True
    return False


def parse_story_output(raw_text):
    """
    Extracts title and formatted paragraphs from the model output.
    """
    raw_text = raw_text.strip()
    title = "Untitled Horror"
    story = raw_text

    # Match patterns like: Title: <Title> or **Title:** <Title> or # <Title>
    title_match = re.search(r'^(?:#+\s*|\*{0,2}Title:?\*{0,2}\s*)([^\n]+)', raw_text, re.IGNORECASE | re.MULTILINE)
    if title_match:
        extracted = title_match.group(1).strip()
        # Clean quotes, brackets, and asterisks
        extracted = re.sub(r'^["\'*#\[\]]+|["\'*#\[\]]+$', '', extracted).strip()
        if extracted and len(extracted) < 120:
            title = extracted
            # Remove title line from story
            story = raw_text[:title_match.start()] + raw_text[title_match.end():]
            story = story.strip()

    # Clean any leftover markdown headers at start of story
    story = re.sub(r'^\s*#+\s*.*?\n', '', story).strip()

    # Calculate word count & reading time
    words = len(story.split())
    reading_time_min = max(1, round(words / 180))

    return {
        "title": title,
        "story": story,
        "word_count": words,
        "reading_time_minutes": reading_time_min
    }


@app.route("/")
def index():
    """Renders the main GhostWriter AI single-page interface."""
    return render_template(
        "index.html",
        configured_model=OLLAMA_MODEL,
        categories=VALID_CATEGORIES,
        endings=VALID_ENDINGS
    )


@app.route("/api/health", methods=["GET"])
def health_check():
    """
    Checks the status of the Ollama server and configured AI model.
    Returns:
        JSON with ollama_running, model_available, configured_model, and diagnostics.
    """
    ollama_ok, models = fetch_available_models()

    if not ollama_ok:
        return jsonify({
            "status": "offline",
            "ollama_running": False,
            "model_available": False,
            "configured_model": OLLAMA_MODEL,
            "available_models": [],
            "message": (
                f"Ollama is not running at {OLLAMA_HOST}. "
                "Please start it in your terminal by running: ollama serve"
            )
        }), 200

    model_ready = is_model_installed(OLLAMA_MODEL, models)

    if not model_ready:
        return jsonify({
            "status": "degraded",
            "ollama_running": True,
            "model_available": False,
            "configured_model": OLLAMA_MODEL,
            "available_models": models,
            "message": (
                f"Ollama is running, but model '{OLLAMA_MODEL}' is not found. "
                f"Download it by running: ollama pull {OLLAMA_MODEL}"
            )
        }), 200

    return jsonify({
        "status": "healthy",
        "ollama_running": True,
        "model_available": True,
        "configured_model": OLLAMA_MODEL,
        "available_models": models,
        "message": f"Ollama is running with model '{OLLAMA_MODEL}' ready."
    }), 200


@app.route("/api/models", methods=["GET"])
def list_models():
    """Returns available local models in Ollama."""
    ollama_ok, models = fetch_available_models()
    return jsonify({
        "ollama_running": ollama_ok,
        "configured_model": OLLAMA_MODEL,
        "models": models
    })


@app.route("/api/generate", methods=["POST"])
def generate_story():
    """
    Generates a personalized horror story based on user prompt, category, and ending.
    """
    data = request.get_json(silent=True) or {}

    user_prompt = (data.get("prompt") or "").strip()
    category = (data.get("category") or "Ghost Stories").strip()
    ending = (data.get("ending") or "Terrifying").strip()
    model_override = (data.get("model") or "").strip()

    # Validation
    if not user_prompt:
        return jsonify({
            "success": False,
            "error": "Please provide a story idea or premise before summoning the spirits."
        }), 400

    if len(user_prompt) > 1000:
        return jsonify({
            "success": False,
            "error": "Story premise is too long. Please keep it under 1000 characters."
        }), 400

    if category not in VALID_CATEGORIES:
        category = "Ghost Stories"

    if ending not in VALID_ENDINGS:
        ending = "Terrifying"

    # Select model
    target_model = model_override if model_override else OLLAMA_MODEL

    # Verify Ollama availability
    ollama_ok, available_models = fetch_available_models()
    if not ollama_ok:
        return jsonify({
            "success": False,
            "error": (
                f"Cannot connect to Ollama at {OLLAMA_HOST}. "
                "Ensure Ollama is running locally with 'ollama serve'."
            )
        }), 503

    if not is_model_installed(target_model, available_models):
        return jsonify({
            "success": False,
            "error": (
                f"Model '{target_model}' is not available locally. "
                f"Run 'ollama pull {target_model}' in your terminal to install it."
            )
        }), 400

    # Build prompt instructions
    tone_guideline = CATEGORY_TONE_MAP.get(category, "")
    ending_guideline = ENDING_INSTRUCTION_MAP.get(ending, "")

    system_instruction = (
        "You are GhostWriter AI, an acclaimed master of horror fiction. "
        "You write atmospheric, gripping horror stories with visceral sensory detail, "
        "mounting tension, and psychological or supernatural dread. "
        "Write with eloquence and gothic depth. "
        "Strictly adhere to the user's selected category and ending instructions.\n\n"
        "OUTPUT FORMAT REQUIREMENT:\n"
        "Start your response with the title on the very first line:\n"
        "Title: [An atmospheric, eerie title]\n\n"
        "Then follow with the complete story in 4 to 6 vivid, well-crafted paragraphs. "
        "Do not include conversational banter, notes, or meta explanations."
    )

    user_instruction = (
        f"HORROR CATEGORY: {category}\n"
        f"ATMOSPHERE & TONE: {tone_guideline}\n\n"
        f"ENDING TYPE: {ending}\n"
        f"CLIMAX & RESOLUTION REQUIREMENT: {ending_guideline}\n\n"
        f"STORY PREMISE:\n\"{user_prompt}\"\n\n"
        "Write the complete horror story now, ensuring the pacing builds dread smoothly "
        "and resolves decisively according to the chosen ending."
    )

    ollama_payload = {
        "model": target_model,
        "prompt": user_instruction,
        "system": system_instruction,
        "stream": False,
        "options": {
            "temperature": 0.85,
            "top_p": 0.9,
            "num_predict": 850
        }
    }

    start_time = time.time()
    try:
        logger.info(f"Generating story with model '{target_model}', category '{category}', ending '{ending}'")
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json=ollama_payload,
            timeout=REQUEST_TIMEOUT
        )

        if resp.status_code != 200:
            logger.error(f"Ollama API returned status {resp.status_code}: {resp.text}")
            return jsonify({
                "success": False,
                "error": f"Ollama generation failed (HTTP {resp.status_code}): {resp.text}"
            }), 502

        result_data = resp.json()
        raw_story = result_data.get("response", "")

        if not raw_story.strip():
            return jsonify({
                "success": False,
                "error": "The local AI returned an empty response. Please try again."
            }), 500

        elapsed = round(time.time() - start_time, 2)
        parsed = parse_story_output(raw_story)

        logger.info(f"Story generated in {elapsed}s: '{parsed['title']}' ({parsed['word_count']} words)")

        return jsonify({
            "success": True,
            "title": parsed["title"],
            "story": parsed["story"],
            "category": category,
            "ending": ending,
            "model": target_model,
            "word_count": parsed["word_count"],
            "reading_time_minutes": parsed["reading_time_minutes"],
            "generation_time_seconds": elapsed
        })

    except requests.exceptions.Timeout:
        logger.error(f"Story generation timed out after {REQUEST_TIMEOUT}s")
        return jsonify({
            "success": False,
            "error": (
                f"Story generation timed out after {REQUEST_TIMEOUT} seconds. "
                "Your local machine might be under heavy load. Please try again with a shorter prompt."
            )
        }), 504

    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to Ollama during generation.")
        return jsonify({
            "success": False,
            "error": "Connection to Ollama was lost. Ensure 'ollama serve' is active."
        }), 503

    except Exception as e:
        logger.exception("Unexpected error during story generation")
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("true", "1")

    print("\n" + "=" * 60)
    print("[*] GHOSTWRITER AI - Stories from the Other Side")
    print("=" * 60)
    print(f" * Server running on: http://{host}:{port}")
    print(f" * Configured Ollama Model: {OLLAMA_MODEL}")
    print(f" * Ollama Host: {OLLAMA_HOST}")
    print("=" * 60 + "\n")

    app.run(host=host, port=port, debug=debug)

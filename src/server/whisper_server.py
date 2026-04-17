"""
NXS+ Local Whisper Transcription Server
========================================
Optional local speech-to-text server using faster-whisper (CTranslate2-optimised).
Exposes a single POST endpoint at /transcribe that accepts audio blobs from the
NXS+ browser application and returns transcribed text.

Requirements
------------
    pip install faster-whisper fastapi uvicorn python-multipart

Usage
-----
    python whisper_server.py

    # Or with a specific model size:
    MODEL_SIZE=large-v2 python whisper_server.py

    # Or with GPU acceleration (requires CUDA):
    DEVICE=cuda python whisper_server.py

The server starts at http://localhost:8765
NXS+ auto-detects it on launch and uses it if available.

Model sizes
-----------
    tiny     — fastest, lowest accuracy (~75MB)
    base     — good balance for most use cases (~145MB)
    small    — recommended for research use (~465MB)
    medium   — high accuracy (~1.5GB)
    large-v2 — best accuracy (~3GB), requires more RAM
"""

import os
import io
import tempfile
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ── Configuration ─────────────────────────────────────────────────────────────

MODEL_SIZE = os.getenv("MODEL_SIZE", "base")       # tiny | base | small | medium | large-v2
DEVICE     = os.getenv("DEVICE", "cpu")            # cpu | cuda
COMPUTE    = os.getenv("COMPUTE_TYPE", "int8")     # int8 | float16 | float32
HOST       = os.getenv("HOST", "127.0.0.1")
PORT       = int(os.getenv("PORT", "8765"))
LANGUAGE   = os.getenv("LANGUAGE", None)           # None = auto-detect; or e.g. "en", "zh"

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("nxs-whisper")

# ── Model loading ─────────────────────────────────────────────────────────────

log.info(f"Loading faster-whisper model: {MODEL_SIZE} on {DEVICE} ({COMPUTE})")
try:
    from faster_whisper import WhisperModel
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE)
    log.info("Model loaded successfully.")
except ImportError:
    log.error("faster-whisper not installed. Run: pip install faster-whisper")
    raise

# ── FastAPI app ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="NXS+ Whisper Transcription Server",
    description="Local speech-to-text for the NXS+ Sphere Network browser application.",
    version="1.0.0"
)

# Allow requests from the browser (file:// and localhost origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    """Health check — NXS+ uses this to detect server availability on launch."""
    return {
        "status": "ok",
        "model": MODEL_SIZE,
        "device": DEVICE,
        "server": "NXS+ Whisper Transcription Server v1.0.0"
    }


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """
    Transcribe an audio file to text.
    
    Accepts: WebM/Opus, OGG, MP4, WAV, or any format supported by ffmpeg.
    Returns: JSON with 'text' field containing the transcription.
    
    Example (browser):
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        const res = await fetch('http://localhost:8765/transcribe', {
            method: 'POST',
            body: formData
        });
        const { text } = await res.json();
    """
    if not audio.filename:
        raise HTTPException(status_code=400, detail="No audio file provided")

    log.info(f"Transcribing: {audio.filename} ({audio.content_type})")

    # Write to a temp file (faster-whisper requires a file path)
    suffix = Path(audio.filename).suffix or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        contents = await audio.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        segments, info = model.transcribe(
            tmp_path,
            language=LANGUAGE,
            beam_size=5,
            vad_filter=True,            # filter out non-speech regions
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        text = " ".join(segment.text.strip() for segment in segments)
        detected_lang = info.language
        duration = info.duration

        log.info(f"Transcribed ({detected_lang}, {duration:.1f}s): {text[:80]}{'...' if len(text) > 80 else ''}")

        return {
            "text": text,
            "language": detected_lang,
            "duration_seconds": round(duration, 2),
            "model": MODEL_SIZE
        }

    except Exception as e:
        log.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")
    finally:
        os.unlink(tmp_path)


@app.get("/models")
def list_models():
    """List available model sizes and their approximate disk sizes."""
    return {
        "current": MODEL_SIZE,
        "available": [
            {"name": "tiny",     "size_mb": 75,   "speed": "fastest", "accuracy": "basic"},
            {"name": "base",     "size_mb": 145,  "speed": "fast",    "accuracy": "good"},
            {"name": "small",    "size_mb": 465,  "speed": "moderate","accuracy": "good"},
            {"name": "medium",   "size_mb": 1500, "speed": "slow",    "accuracy": "high"},
            {"name": "large-v2", "size_mb": 3000, "speed": "slowest", "accuracy": "best"},
        ]
    }


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    log.info(f"Starting NXS+ Whisper server at http://{HOST}:{PORT}")
    log.info(f"NXS+ will auto-detect this server on launch.")
    log.info(f"Press Ctrl+C to stop.")
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning")

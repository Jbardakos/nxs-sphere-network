#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║   ∅  SPHERE NETWORK — LOCAL WHISPER SETUP   ║
║   Double-click this file (or run it once)   ║
║   Everything installs and starts itself.    ║
╚══════════════════════════════════════════════╝

  What this does:
    1. Installs Python dependencies (pip)
    2. Downloads the Whisper speech model (~240MB, first run only)
    3. Starts a local server on http://localhost:8765
    4. Opens your browser automatically
    5. [4] key now records mic → transcribes locally, FREE, offline

  Requirements:
    - Python 3.9+  (check: python --version)
    - ~500 MB free disk space (for model)
    - Microphone

  Model sizes (edit MODEL_SIZE below):
    "tiny"   — fastest, ~75MB,  okay accuracy
    "small"  — fast,   ~240MB, good accuracy  ← DEFAULT
    "medium" — slower, ~770MB, very good
    "large"  — slow,   ~1.5GB, best (needs 4GB+ RAM)

  To stop the server: Ctrl+C in this terminal window.
"""

# ─── CONFIGURE HERE ───────────────────────────────────────────────────────────
MODEL_SIZE  = "small"   # tiny / small / medium / large
PORT        = 8765
# ──────────────────────────────────────────────────────────────────────────────

import sys
import os
import subprocess
import threading
import time
import webbrowser
import tempfile
from pathlib import Path

HERE = Path(__file__).parent.resolve()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — INSTALL DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════

DEPS = [
    "faster-whisper",
    "fastapi",
    "uvicorn[standard]",
    "python-multipart",
]

print()
print("  ∅  SPHERE NETWORK — starting setup")
print("  " + "─" * 42)

def pip_install(package):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", package,
         "-q", "--disable-pip-version-check"],
        capture_output=True, text=True
    )
    return result.returncode == 0

for dep in DEPS:
    print(f"  →  {dep:<28}", end="", flush=True)
    ok = pip_install(dep)
    print("✓" if ok else "⚠  (may already be installed)")

print()

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — IMPORT LIBS (after install)
# ══════════════════════════════════════════════════════════════════════════════

try:
    from fastapi import FastAPI, UploadFile, File
    from fastapi.responses import HTMLResponse, JSONResponse
    import uvicorn
except ImportError as e:
    print(f"\n  ⚠  Import failed: {e}")
    print("     Try running: pip install fastapi uvicorn[standard] python-multipart")
    input("\n  Press Enter to exit...")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — LOAD WHISPER MODEL
# ══════════════════════════════════════════════════════════════════════════════

print(f"  →  Loading Whisper '{MODEL_SIZE}' model...", end="", flush=True)
print()
print(f"       (First run downloads model files — please wait)")
print()

try:
    from faster_whisper import WhisperModel
    # HuggingFace mirror hint for China — set env var if needed
    # os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
    whisper_model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    print(f"  ✓  Whisper '{MODEL_SIZE}' ready")
except Exception as e:
    print(f"\n  ⚠  Could not load Whisper model: {e}")
    print("     If you're in China, HuggingFace may be blocked.")
    print("     Try: set HF_ENDPOINT=https://hf-mirror.com  (then rerun)")
    input("\n  Press Enter to exit...")
    sys.exit(1)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — LOAD & PATCH THE HTML
# ══════════════════════════════════════════════════════════════════════════════

html_path = HERE / "appearance-trigger.html"
if not html_path.exists():
    print(f"\n  ⚠  Cannot find appearance-trigger.html")
    print(f"     Expected alongside this script: {html_path}")
    input("\n  Press Enter to exit...")
    sys.exit(1)

html = html_path.read_text(encoding="utf-8")
original_len = len(html)

# ── Patch 1: Remove OpenAI API key check and replace fetch endpoint ──
OLD_FETCH = """      const apiKey=apiKeyInput.value.trim();
      if(!apiKey){setStatus('⚠  NO API KEY — WORDS LOST');resolve();return;}
      setStatus('◌  TRANSCRIBING...');
      const mime=mediaRec.mimeType||'audio/webm';
      const blob=new Blob(audioChunks,{type:mime});
      const fd=new FormData();
      fd.append('file',blob,'rec.'+mimeToExt(mime));
      fd.append('model','whisper-1');
      try{
        const r=await fetch('https://api.openai.com/v1/audio/transcriptions',{
          method:'POST', headers:{'Authorization':'Bearer '+apiKey}, body:fd
        });"""

NEW_FETCH = """      setStatus('◌  TRANSCRIBING LOCALLY...');
      const mime=mediaRec.mimeType||'audio/webm';
      const blob=new Blob(audioChunks,{type:mime});
      const fd=new FormData();
      fd.append('file',blob,'rec.'+mimeToExt(mime));
      try{
        const r=await fetch('/transcribe',{method:'POST',body:fd});"""

html = html.replace(OLD_FETCH, NEW_FETCH)

# ── Patch 2: Remove the apiKeyInput guard (appears twice in keydown/keyup) ──
html = html.replace(
    "  if(document.activeElement===apiKeyInput)return;\n",
    ""
)

# ── Patch 3: Replace API key input UI with local server status ──
OLD_KEY_UI = """  <div id="key-wrap">
    <div id="key-label">WHISPER API KEY</div>
    <input id="api-key-input" type="password" placeholder="sk-..." spellcheck="false" autocomplete="off">
  </div>"""

NEW_KEY_UI = f"""  <div id="key-wrap">
    <div id="key-label">LOCAL WHISPER · {MODEL_SIZE.upper()} MODEL</div>
    <div style="color:rgba(255,255,255,0.28);font-size:7px;letter-spacing:0.16em;padding:3px 0;font-family:Share Tech Mono,monospace;">● OFFLINE · PORT {PORT}</div>
  </div>"""

html = html.replace(OLD_KEY_UI, NEW_KEY_UI)

# Verify patches applied
patched = len(html) != original_len or "/transcribe" in html
if not patched:
    print("  ⚠  HTML patching may have partially failed — the app will still run")
    print("     but [4] recording may not work without an API key.")
else:
    print("  ✓  HTML patched for local Whisper")

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 5 — FASTAPI SERVER
# ══════════════════════════════════════════════════════════════════════════════

app = FastAPI(title="Sphere Network")

@app.get("/", response_class=HTMLResponse)
async def index():
    return html

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Receive audio blob, transcribe with local Whisper, return {text}."""
    filename = file.filename or "audio.webm"
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "webm"

    # Write to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        data = await file.read()
        tmp.write(data)
        tmp_path = tmp.name

    try:
        segments, info = whisper_model.transcribe(
            tmp_path,
            beam_size=5,
            vad_filter=True,          # skip silence chunks
            vad_parameters={"min_silence_duration_ms": 300},
        )
        words = []
        for seg in segments:
            words.extend(seg.text.strip().split())
        text = " ".join(words)
        print(f"  ▶  Transcribed: {text[:80]}{'…' if len(text)>80 else ''}")
        return {"text": text}
    except Exception as e:
        print(f"  ⚠  Transcription error: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass

@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_SIZE, "port": PORT}

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 6 — OPEN BROWSER + RUN
# ══════════════════════════════════════════════════════════════════════════════

def open_browser():
    time.sleep(1.8)  # wait for server to be ready
    url = f"http://localhost:{PORT}"
    print(f"\n  ∅  Opening browser → {url}")
    webbrowser.open(url)

threading.Thread(target=open_browser, daemon=True).start()

print()
print("  " + "═" * 42)
print(f"  ∅  Server ready at http://localhost:{PORT}")
print(f"     Whisper model : {MODEL_SIZE}")
print(f"     Transcription : LOCAL (free, offline)")
print(f"     Stop server   : Ctrl+C")
print("  " + "═" * 42)
print()

uvicorn.run(
    app,
    host="127.0.0.1",
    port=PORT,
    log_level="warning",   # quiet — only errors shown
)

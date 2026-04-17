#!/usr/bin/env python3
"""
∅ SPHERE NETWORK — one-click launcher
Run:  python start.py
      python start.py --model small   (tiny/base/small/medium/large-v2/large-v3)
      python start.py --port 8765
      python start.py --no-browser
"""

import sys, os, subprocess, importlib, argparse, pathlib, time, threading, webbrowser, re

p = argparse.ArgumentParser()
p.add_argument("--model",      default="small",
               choices=["tiny","base","small","medium","large-v2","large-v3"])
p.add_argument("--port",       default=8765, type=int)
p.add_argument("--no-browser", action="store_true")
p.add_argument("--device",     default="cpu")
args = p.parse_args()

PORT  = args.port
MODEL = args.model
DEV   = args.device

GR="\033[92m"; YL="\033[93m"; RD="\033[91m"; CY="\033[96m"; RS="\033[0m"; BD="\033[1m"
def ok(m):   print(f"  {GR}✓{RS}  {m}")
def info(m): print(f"  {CY}·{RS}  {m}")
def err(m):  print(f"\n  {RD}✗  {m}{RS}\n"); sys.exit(1)

print(f"\n{BD}  ∅ SPHERE NETWORK — local Whisper launcher{RS}")
print(f"  {'─'*44}")

if sys.version_info < (3, 8):
    err(f"Python 3.8+ required (you have {sys.version_info.major}.{sys.version_info.minor})")
ok(f"Python {sys.version_info.major}.{sys.version_info.minor}")

# ── auto-install ──────────────────────────────────────────────────────────────
REQUIRED = {
    "faster_whisper": "faster-whisper",
    "fastapi":        "fastapi",
    "uvicorn":        "uvicorn[standard]",
    "multipart":      "python-multipart",
}

def pip_install(pkg):
    info(f"Installing {pkg} ...")
    for flags in [[], ["--break-system-packages"], ["--user"]]:
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", pkg] + flags,
            capture_output=True
        )
        if r.returncode == 0:
            return True
    return False

for import_name, pip_name in REQUIRED.items():
    try:
        importlib.import_module(import_name)
        ok(pip_name)
    except ImportError:
        if pip_install(pip_name):
            ok(f"{pip_name} (just installed)")
        else:
            print(f"\n  {RD}Could not auto-install '{pip_name}'{RS}")
            print(f"  Run this first, then re-run start.py:\n")
            print(f"    {CY}python3 -m venv .venv && source .venv/bin/activate{RS}")
            print(f"    {CY}python start.py{RS}\n")
            sys.exit(1)

# ── find HTML ─────────────────────────────────────────────────────────────────
SCRIPT_DIR = pathlib.Path(__file__).parent
html_path = None
for name in ["appearance-trigger.html", "sphere-network.html", "index.html"]:
    c = SCRIPT_DIR / name
    if c.exists():
        html_path = c
        break

if html_path is None:
    err("HTML file not found. Place appearance-trigger.html next to start.py")
ok(f"HTML → {html_path.name}")

# ── inject config into the <script id="sphere-cfg"> block ────────────────────
# This is the ONLY string we replace — a clearly delimited block we control.
html_raw = html_path.read_text(encoding="utf-8")

LOCAL_URL = f"http://localhost:{PORT}/transcribe"

new_cfg = f"""<script id="sphere-cfg">
window.SPHERE_CFG = {{
  transcribeURL: '{LOCAL_URL}',
  localMode: true,
}};
</script>"""

patched, n = re.subn(
    r'<script id="sphere-cfg">.*?</script>',
    new_cfg,
    html_raw,
    flags=re.DOTALL
)

if n == 0:
    err(
        "Could not find <script id=\"sphere-cfg\"> in the HTML.\n"
        "  Make sure you're using the latest appearance-trigger.html from this session."
    )
ok("Config injected (local mode, no API key needed)")

# ── load Whisper ──────────────────────────────────────────────────────────────
print()
info(f"Loading Whisper '{MODEL}' on {DEV} ...")
info( "(first run downloads model weights — may take a minute)")
print()

from faster_whisper import WhisperModel
compute = "int8" if DEV == "cpu" else "float16"
try:
    wmodel = WhisperModel(MODEL, device=DEV, compute_type=compute)
    ok(f"Whisper '{MODEL}' ready ({DEV}/{compute})")
except Exception as e:
    err(f"Failed to load Whisper: {e}")

# ── FastAPI app ───────────────────────────────────────────────────────────────
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import tempfile, shutil

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

@app.get("/", response_class=HTMLResponse)
async def serve():
    return HTMLResponse(content=patched)

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = pathlib.Path(file.filename or "audio.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        segs, _ = wmodel.transcribe(tmp_path, beam_size=5)
        text = " ".join(s.text.strip() for s in segs)
        return JSONResponse({"text": text})
    except Exception as e:
        return JSONResponse({"error": str(e), "text": ""}, status_code=500)
    finally:
        os.unlink(tmp_path)

@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL}

# ── launch ────────────────────────────────────────────────────────────────────
print()
print(f"  {BD}App{RS}   http://localhost:{PORT}/")
print(f"  {BD}API{RS}   http://localhost:{PORT}/transcribe")
print(f"\n  {YL}Press Ctrl+C to stop{RS}\n")

if not args.no_browser:
    def _open():
        time.sleep(1.8)
        webbrowser.open(f"http://localhost:{PORT}")
    threading.Thread(target=_open, daemon=True).start()

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="warning")

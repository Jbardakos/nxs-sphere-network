#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║   ∅  SPHERE NETWORK — LOCAL WHISPER SETUP            ║
║   One-click install + launch                         ║
║   Works on macOS, Linux, Windows                     ║
╚══════════════════════════════════════════════════════╝

Usage:
    python3 setup.py          ← install + launch (first time)
    python3 setup.py --run    ← just launch (already installed)
    python3 setup.py --stop   ← kill the server
"""

import sys, os, subprocess, time, webbrowser, pathlib, shutil, signal

HERE   = pathlib.Path(__file__).parent.resolve()
VENV   = HERE / "sphere-env"
PORT   = 8765
PID_F  = HERE / ".sphere-server.pid"

# ─── colour helpers ───────────────────────────────────
def c(code, txt): return f"\033[{code}m{txt}\033[0m"
OK  = lambda t: print(c("92", f"  ✓  {t}"))
ERR = lambda t: print(c("91", f"  ✗  {t}"))
INF = lambda t: print(c("94", f"  ·  {t}"))
HDR = lambda t: print(c("97", f"\n{t}"))

# ─── python paths ─────────────────────────────────────
def venv_python():
    if sys.platform == "win32":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"

def venv_uvicorn():
    if sys.platform == "win32":
        return VENV / "Scripts" / "uvicorn.exe"
    return VENV / "bin" / "uvicorn"

# ════════════════════════════════════════════════════════
#  SERVER CODE  (written to server.py)
# ════════════════════════════════════════════════════════
SERVER_CODE = r"""
import os, pathlib, tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# ── Load model once at startup ──────────────────────
from faster_whisper import WhisperModel
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "small")
print(f"[whisper] Loading model '{MODEL_SIZE}' on CPU …")
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
print(f"[whisper] Model ready.")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve the HTML app ──────────────────────────────
HTML_PATH = pathlib.Path(__file__).parent / "sphere-network.html"

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(HTML_PATH.read_text(encoding="utf-8"))

# ── Transcription endpoint ──────────────────────────
@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    suffix = "." + (file.filename.rsplit(".", 1)[-1] if "." in file.filename else "webm")
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    try:
        segments, _ = model.transcribe(tmp_path, beam_size=5)
        text = " ".join(s.text for s in segments).strip()
        return JSONResponse({"text": text})
    except Exception as e:
        return JSONResponse({"text": "", "error": str(e)}, status_code=500)
    finally:
        try: os.unlink(tmp_path)
        except: pass
"""

# ════════════════════════════════════════════════════════
#  HTML APP  (the sphere network, pointing to localhost)
# ════════════════════════════════════════════════════════
# Read from sphere-network.html if it exists next to this script,
# otherwise write the embedded version below.
def get_html_path():
    p = HERE / "sphere-network.html"
    if not p.exists():
        # write embedded HTML
        p.write_text(SPHERE_HTML, encoding="utf-8")
        OK("sphere-network.html written")
    return p

# ════════════════════════════════════════════════════════
#  INSTALL
# ════════════════════════════════════════════════════════
PACKAGES = [
    "faster-whisper",
    "fastapi",
    "uvicorn[standard]",
    "python-multipart",
]

def create_venv():
    HDR("Creating virtual environment …")
    subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)
    OK(f"venv at {VENV}")

def install_packages():
    HDR("Installing packages (first time may take 2–5 min) …")
    pip = str(venv_python())
    for pkg in PACKAGES:
        INF(f"Installing {pkg} …")
        subprocess.run([pip, "-m", "pip", "install", "--quiet", pkg], check=True)
        OK(pkg)

def write_server():
    p = HERE / "server.py"
    p.write_text(SERVER_CODE.lstrip(), encoding="utf-8")
    OK("server.py written")

# ════════════════════════════════════════════════════════
#  LAUNCH
# ════════════════════════════════════════════════════════
def server_running():
    import socket
    try:
        s = socket.create_connection(("127.0.0.1", PORT), timeout=1)
        s.close(); return True
    except: return False

def launch_server():
    HDR("Starting local Whisper server …")
    env = os.environ.copy()
    env["WHISPER_MODEL"] = "small"   # change to "medium" for better accuracy

    proc = subprocess.Popen(
        [str(venv_uvicorn()), "server:app",
         "--host", "127.0.0.1", "--port", str(PORT), "--log-level", "warning"],
        cwd=str(HERE), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    PID_F.write_text(str(proc.pid))

    INF("Waiting for server to be ready …")
    for _ in range(30):
        if server_running(): break
        if proc.poll() is not None:
            err = proc.stderr.read().decode()
            ERR(f"Server failed to start:\n{err}")
            sys.exit(1)
        time.sleep(0.5)
    else:
        ERR("Server did not start in time.")
        sys.exit(1)

    OK(f"Server running at http://localhost:{PORT}")
    return proc

def open_browser():
    HDR("Opening browser …")
    time.sleep(0.4)
    webbrowser.open(f"http://localhost:{PORT}")
    OK("Browser opened")

def stop_server():
    if not PID_F.exists():
        INF("No running server found."); return
    pid = int(PID_F.read_text())
    try:
        os.kill(pid, signal.SIGTERM)
        PID_F.unlink()
        OK(f"Server (pid {pid}) stopped.")
    except ProcessLookupError:
        INF("Server was not running."); PID_F.unlink()

# ════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════
def main():
    print(c("97", """
╔══════════════════════════════════════════════════════╗
║   ∅  SPHERE NETWORK — LOCAL WHISPER SETUP            ║
╚══════════════════════════════════════════════════════╝"""))

    args = sys.argv[1:]

    if "--stop" in args:
        stop_server(); return

    # Check Python version
    if sys.version_info < (3, 9):
        ERR(f"Python 3.9+ required (you have {sys.version})"); sys.exit(1)
    OK(f"Python {sys.version.split()[0]}")

    if "--run" not in args:
        # Full install
        if VENV.exists():
            INF("Virtual environment already exists — skipping install.")
            INF("Use --run to skip this check, or delete sphere-env/ to reinstall.")
        else:
            create_venv()
            install_packages()

    write_server()
    get_html_path()

    INF(f"Whisper model: small (fast, good quality)")
    INF(f"Change to 'medium' by editing WHISPER_MODEL in server.py for better accuracy")
    INF(f"")

    if server_running():
        INF(f"Server already running at http://localhost:{PORT}")
        open_browser()
        return

    proc = launch_server()
    open_browser()

    print(c("94", f"""
  ┌──────────────────────────────────────────────────┐
  │  ∅  SPHERE NETWORK is running                    │
  │  http://localhost:{PORT}                            │
  │                                                  │
  │  Controls:                                       │
  │  [1] Hold → Vocal trigger                        │
  │  [2] Hold in window → Size → Appear at cursor   │
  │  [3] With 2 selected → Connect                  │
  │  [4] Hold on selected sphere → Record voice     │
  │  [5] Hold on selected sphere → Play words       │
  │  Middle drag → Orbit camera                     │
  │  Scroll → Zoom · Space+drag → Pan              │
  │                                                  │
  │  Press Ctrl+C to stop the server                │
  └──────────────────────────────────────────────────┘
"""))

    try:
        while True:
            if proc.poll() is not None:
                err = proc.stderr.read().decode()
                ERR(f"Server exited unexpectedly:\n{err}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        INF("Shutting down …")
        proc.terminate()
        PID_F.unlink(missing_ok=True)
        OK("Done. Goodbye.")

if __name__ == "__main__":
    main()


# ════════════════════════════════════════════════════════
#  EMBEDDED HTML  (auto-written if sphere-network.html
#  is not found next to this script)
# ════════════════════════════════════════════════════════
SPHERE_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>∅ SPHERE NETWORK</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Raleway:wght@200;300&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 100%; height: 100%; background: #000; overflow: hidden; cursor: crosshair; }
  canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; display: block; }
  #flash { position: fixed; inset: 0; background: #fff; opacity: 0; pointer-events: none; z-index: 30; }
  #labels-container { position: fixed; inset: 0; pointer-events: none; z-index: 15; overflow: hidden; }
  .sphere-label { position: absolute; font-family: 'Share Tech Mono', monospace; font-size: 8.5px; color: rgba(255,255,255,0.20); letter-spacing: 0.22em; text-transform: uppercase; white-space: nowrap; transform: translate(-50%, 0); pointer-events: none; user-select: none; line-height: 1.9; transition: color 0.25s; }
  .sphere-label.sel { color: rgba(255,255,255,0.68); }
  .sphere-label.rec { color: rgba(255,80,80,0.82); }
  .sphere-id { font-size: 7px; opacity: 0.4; display: block; letter-spacing: 0.3em; }
  .sphere-term { font-size: 8px; letter-spacing: 0.18em; }
  #word-display { position: fixed; pointer-events: none; z-index: 25; font-family: 'Raleway', sans-serif; font-weight: 200; font-size: 26px; letter-spacing: 0.20em; text-transform: uppercase; color: rgba(255,255,255,0.88); text-shadow: 0 0 50px rgba(255,255,255,0.12); transform: translate(-50%, -50%); opacity: 0; transition: opacity 0.45s ease; white-space: nowrap; }
  #word-display.vis { opacity: 1; }
  #rec-pill { position: fixed; top: 22px; left: 50%; transform: translateX(-50%); font-family: 'Share Tech Mono', monospace; font-size: 8px; letter-spacing: 0.28em; text-transform: uppercase; color: rgba(255,80,80,0.92); border: 1px solid rgba(255,80,80,0.28); padding: 5px 18px 5px 24px; border-radius: 2px; pointer-events: none; z-index: 40; opacity: 0; transition: opacity 0.2s; display: flex; align-items: center; gap: 10px; }
  #rec-pill.show { opacity: 1; }
  #rec-dot { width: 6px; height: 6px; border-radius: 50%; background: rgba(255,80,80,1); box-shadow: 0 0 6px rgba(255,80,80,0.8); animation: blink 0.65s ease-in-out infinite; }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.15} }
  #hud { position: fixed; inset: 0; pointer-events: none; font-family: 'Share Tech Mono', monospace; color: rgba(255,255,255,0.75); z-index: 20; }
  .brk { position: absolute; width: 15px; height: 15px; opacity: 0.09; }
  .brk-tl { top: 20px; left: 20px; border-top: 1px solid #fff; border-left: 1px solid #fff; }
  .brk-tr { top: 20px; right: 20px; border-top: 1px solid #fff; border-right: 1px solid #fff; }
  .brk-bl { bottom: 20px; left: 20px; border-bottom: 1px solid #fff; border-left: 1px solid #fff; }
  .brk-br { bottom: 20px; right: 20px; border-bottom: 1px solid #fff; border-right: 1px solid #fff; }
  #triggers { position: absolute; top: 26px; left: 32px; display: flex; flex-direction: column; gap: 7px; }
  .trigger-row { display: flex; align-items: center; gap: 9px; font-size: 8.5px; letter-spacing: 0.18em; text-transform: uppercase; opacity: 0.15; transition: opacity 0.12s; }
  .trigger-row.active { opacity: 1; } .trigger-row.success { opacity: 1; } .trigger-row.error { opacity: 0.50; }
  .dot { width: 5px; height: 5px; border-radius: 50%; background: rgba(255,255,255,0.10); border: 1px solid rgba(255,255,255,0.14); transition: background 0.1s, box-shadow 0.1s; flex-shrink: 0; }
  .trigger-row.active .dot { background: #fff; box-shadow: 0 0 7px #fff; }
  .trigger-row.success .dot { background: #fff; box-shadow: 0 0 12px #fff, 0 0 28px rgba(255,255,255,0.5); }
  .trigger-row.error .dot { background: #777; }
  .trigger-row.rec-row .dot { background: rgba(255,80,80,1); box-shadow: 0 0 8px rgba(255,80,80,0.9); animation: blink 0.65s ease-in-out infinite; }
  #status { position: absolute; bottom: 84px; left: 50%; transform: translateX(-50%); font-size: 8.5px; letter-spacing: 0.28em; text-transform: uppercase; opacity: 0.30; white-space: nowrap; transition: opacity 0.2s; }
  #status.dim { opacity: 0.10; }
  #timing-wrap { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); width: 280px; opacity: 0; transition: opacity 0.3s; pointer-events: none; }
  #timing-wrap.show { opacity: 1; }
  #t-label { font-size: 7px; letter-spacing: 0.20em; text-transform: uppercase; opacity: 0.20; text-align: center; margin-bottom: 8px; }
  #t-bar { width: 100%; height: 1px; background: rgba(255,255,255,0.04); position: relative; }
  #zone-early { position: absolute; top: -1px; left: 0; width: 33.33%; height: 3px; background: rgba(140,140,140,0.10); }
  #zone-valid { position: absolute; top: -1px; left: 33.33%; width: 66.67%; height: 3px; background: rgba(255,255,255,0.07); }
  #t-cursor { position: absolute; top: -5px; width: 1px; height: 11px; background: rgba(255,255,255,0.55); left: 0%; }
  #t-marks { display: flex; justify-content: space-between; margin-top: 6px; font-size: 6.5px; opacity: 0.13; }
  #size-wrap { position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); width: 240px; opacity: 0; transition: opacity 0.2s; pointer-events: none; display: flex; flex-direction: column; align-items: center; gap: 8px; }
  #size-wrap.show { opacity: 1; }
  #size-label { font-size: 7px; letter-spacing: 0.22em; text-transform: uppercase; opacity: 0.20; }
  #size-track { width: 100%; height: 1px; background: rgba(255,255,255,0.04); position: relative; }
  #size-fill { position: absolute; top: -1px; left: 0; height: 3px; width: 0%; background: rgba(255,255,255,0.50); }
  #size-val { font-size: 8px; letter-spacing: 0.15em; opacity: 0.22; }
  #net-stats { position: absolute; bottom: 24px; right: 32px; font-size: 7.5px; letter-spacing: 0.14em; text-align: right; opacity: 0.13; line-height: 2.2; text-transform: uppercase; }
  #sel-info { position: absolute; top: 50%; right: 32px; transform: translateY(-50%); font-size: 7.5px; letter-spacing: 0.13em; text-transform: uppercase; opacity: 0; transition: opacity 0.22s; line-height: 2.6; text-align: right; }
  #cam-info { position: absolute; top: 26px; right: 32px; text-align: right; font-size: 7px; letter-spacing: 0.11em; line-height: 2.6; opacity: 0.08; text-transform: uppercase; }
  #scanlines { position: fixed; inset: 0; pointer-events: none; z-index: 10; background: repeating-linear-gradient(to bottom, transparent 0, transparent 3px, rgba(0,0,0,0.022) 3px, rgba(0,0,0,0.022) 4px); }
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="labels-container"></div>
<div id="word-display"></div>
<div id="rec-pill"><div id="rec-dot"></div><span id="rec-label">RECORDING</span></div>
<div id="flash"></div>
<div id="scanlines"></div>
<div id="hud">
  <div class="brk brk-tl"></div><div class="brk brk-tr"></div>
  <div class="brk brk-bl"></div><div class="brk brk-br"></div>
  <div id="triggers">
    <div class="trigger-row" id="t1r"><div class="dot"></div><span>[1] VOCAL TRIGGER</span></div>
    <div class="trigger-row" id="t2r"><div class="dot"></div><span>[2] HOLD → SIZE → APPEAR</span></div>
    <div class="trigger-row" id="t3r"><div class="dot"></div><span>[3] CONNECT PAIR</span></div>
    <div class="trigger-row" id="t4r"><div class="dot"></div><span>[4] HOLD → RECORD (LOCAL WHISPER)</span></div>
    <div class="trigger-row" id="t5r"><div class="dot"></div><span>[5] HOLD → PLAY WORDS</span></div>
  </div>
  <div id="status">HOLD [1] TO ACTIVATE VOCAL TRIGGER</div>
  <div id="timing-wrap">
    <div id="t-label">TRIGGER WINDOW · 0 ——————————— 3s</div>
    <div id="t-bar"><div id="zone-early"></div><div id="zone-valid"></div><div id="t-cursor"></div></div>
    <div id="t-marks"><span>0s</span><span>TOO EARLY</span><span>1s VALID →</span><span>3s</span></div>
  </div>
  <div id="size-wrap">
    <div id="size-label">SPHERE MASS — HOLD LONGER</div>
    <div id="size-track"><div id="size-fill"></div></div>
    <div id="size-val">∅ 0.00</div>
  </div>
  <div id="net-stats">NODES <span id="cnt-s">0</span><br>EDGES <span id="cnt-c">0</span></div>
  <div id="sel-info"></div>
  <div id="cam-info">ORBIT MID DRAG<br>ZOOM SCROLL<br>PAN SPC+DRAG<br>SLOW +SHIFT</div>
</div>
<script type="importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"}}</script>
<script type="module">
import * as THREE from 'three';
const canvas=document.getElementById('c');
const renderer=new THREE.WebGLRenderer({canvas,antialias:true});
renderer.setPixelRatio(Math.min(devicePixelRatio,2));
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
renderer.setClearColor(0x000000,1);
const scene=new THREE.Scene();
scene.fog=new THREE.FogExp2(0x000000,0.018);
const camera=new THREE.PerspectiveCamera(52,1,0.05,300);
let camTheta=0,camPhi=Math.PI/2,camRadius=8.0;
const camTarget=new THREE.Vector3();
function applyCam(){const sp=Math.sin(camPhi),cp=Math.cos(camPhi),st=Math.sin(camTheta),ct=Math.cos(camTheta);camera.position.set(camTarget.x+camRadius*sp*st,camTarget.y+camRadius*cp,camTarget.z+camRadius*sp*ct);camera.lookAt(camTarget);camera.updateMatrixWorld();}
applyCam();
function onResize(){renderer.setSize(window.innerWidth,window.innerHeight);camera.aspect=window.innerWidth/window.innerHeight;camera.updateProjectionMatrix();}
onResize();window.addEventListener('resize',onResize);
const mouseNDC=new THREE.Vector2();
window.addEventListener('mousemove',e=>{mouseNDC.x=(e.clientX/window.innerWidth)*2-1;mouseNDC.y=-(e.clientY/window.innerHeight)*2+1;});
scene.add(new THREE.AmbientLight(0x0c0c0c,1));
const keyL=new THREE.PointLight(0xffffff,5,55);keyL.position.set(7,9,8);scene.add(keyL);
const rimL=new THREE.PointLight(0xbbbbbb,2.2,38);rimL.position.set(-7,-5,-7);scene.add(rimL);
const fillL=new THREE.PointLight(0xffffff,1.0,28);fillL.position.set(0,-8,6);scene.add(fillL);
{const N=600,pos=new Float32Array(N*3);for(let i=0;i<N;i++){pos[i*3]=(Math.random()-.5)*70;pos[i*3+1]=(Math.random()-.5)*70;pos[i*3+2]=(Math.random()-.5)*35;}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(pos,3));scene.add(new THREE.Points(g,new THREE.PointsMaterial({color:0xffffff,size:0.015,transparent:true,opacity:0.06})));}
const clamp01=t=>Math.max(0,Math.min(1,t));
const lerp=(a,b,t)=>a+(b-a)*t;
const easeOut3=t=>1-(1-t)**3;
const easeOut5=t=>1-(1-t)**5;
const ANIM_DUR=13/24;
const KF=[[0,0],[0.231,0],[0.385,1.2],[0.462,1],[0.538,1.03],[0.692,1],[1,1]];
function sampleKF(t){for(let i=0;i<KF.length-1;i++){const [t0,s0]=KF[i],[t1,s1]=KF[i+1];if(t<=t1)return lerp(s0,s1,clamp01(i===1?easeOut5((t-t0)/(t1-t0)):(t-t0)/(t1-t0)));}return 1;}
function torusAnim(t,delay=0){const st=clamp01((t-delay)/1.1);if(st<=0)return{scale:.01,op:0};return{scale:lerp(.5,3.2,easeOut3(st)),op:clamp01(st<.12?lerp(0,1,st/.12):lerp(1,0,easeOut3((st-.12)/.88)))};}
function lineAnim(t,idx){const tl=t-(idx%6)*0.030;if(tl<=0)return{outerFrac:0,op:0};return{outerFrac:clamp01(easeOut5(tl/1.0)),op:clamp01(tl<1.0?1.0:1.0-(tl-1.0)/(5/24))};}
const entities=[],meshList=[],connections=[];
let selected=[],entityIdCounter=0;
const labelsEl=document.getElementById('labels-container');
const recPill=document.getElementById('rec-pill');
const recLabelEl=document.getElementById('rec-label');
let isRecording=false,mediaRec=null,audioChunks=[],recordingEnt=null;
function getBestMime(){const ts=['audio/webm;codecs=opus','audio/webm','audio/ogg;codecs=opus','audio/ogg','audio/mp4'];return ts.find(t=>MediaRecorder.isTypeSupported(t))||'';}
function mimeToExt(m){return m.includes('ogg')?'ogg':m.includes('mp4')?'mp4':'webm';}
async function startRecording(ent){
  if(isRecording)return;
  try{
    const stream=await navigator.mediaDevices.getUserMedia({audio:true});
    const mime=getBestMime();
    mediaRec=new MediaRecorder(stream,mime?{mimeType:mime}:{});
    audioChunks=[];
    mediaRec.ondataavailable=e=>{if(e.data.size>0)audioChunks.push(e.data);};
    mediaRec.start(100);
    isRecording=true;recordingEnt=ent;ent.recording=true;
    recPill.classList.add('show');
    recLabelEl.textContent='REC \u2205'+String(ent.id).padStart(2,'0');
    setT4('rec-row');
    setStatus('\u25cf RECORDING \u2014 RELEASE [4] TO TRANSCRIBE');
  }catch(err){setStatus('\u26a0  MIC PERMISSION DENIED');}
}
async function stopRecording(){
  if(!isRecording||!mediaRec)return;
  return new Promise(resolve=>{
    mediaRec.onstop=async()=>{
      const ent=recordingEnt;
      isRecording=false;recordingEnt=null;
      if(ent)ent.recording=false;
      recPill.classList.remove('show');setT4('');
      setStatus('\u25cc  TRANSCRIBING...');
      const mime=mediaRec.mimeType||'audio/webm';
      const blob=new Blob(audioChunks,{type:mime});
      const fd=new FormData();
      fd.append('file',blob,'rec.'+mimeToExt(mime));
      try{
        const r=await fetch('http://localhost:8765/transcribe',{method:'POST',body:fd});
        const d=await r.json();
        if(d.text){
          const words=d.text.trim().split(/\s+/).filter(Boolean);
          if(ent){
            ent.words=[...(ent.words||[]),...words];
            ent.termSpan.textContent=ent.words.slice(0,4).join(' ')+(ent.words.length>4?'\u2026':'');
            setStatus('\u2205'+String(ent.id).padStart(2,'0')+' +'+words.length+' WORDS SAVED');
          }
        }else{setStatus('\u26a0  TRANSCRIPTION EMPTY');}
      }catch(e){setStatus('\u26a0  LOCAL SERVER ERROR \u2014 IS server.py RUNNING?');}
      resolve();
    };
    if(mediaRec.stream)mediaRec.stream.getTracks().forEach(t=>t.stop());
    mediaRec.stop();
  });
}
const wordDisplayEl=document.getElementById('word-display');
let wordPlayEnt=null,wordPlayIdx=0,wordPlayTimer=null,isPlayingWords=false;
function startWordPlay(ent){if(!ent.words||!ent.words.length){setStatus('\u26a0  NO WORDS IN THIS SPHERE');return;}isPlayingWords=true;wordPlayEnt=ent;wordPlayIdx=0;showWord();wordPlayTimer=setInterval(()=>{wordPlayIdx=(wordPlayIdx+1)%ent.words.length;showWord();},2000);}
function showWord(){if(!wordPlayEnt||!wordPlayEnt.words.length)return;wordDisplayEl.textContent=wordPlayEnt.words[wordPlayIdx];wordDisplayEl.classList.add('vis');}
function stopWordPlay(){clearInterval(wordPlayTimer);wordPlayTimer=null;isPlayingWords=false;wordDisplayEl.classList.remove('vis');wordPlayEnt=null;}
function updateWordDisplay(){if(!isPlayingWords||!wordPlayEnt)return;const v=wordPlayEnt.group.position.clone().project(camera);wordDisplayEl.style.left=((v.x*.5+.5)*window.innerWidth)+'px';wordDisplayEl.style.top=((-v.y*.5+.5)*window.innerHeight)+'px';}
function spawnSphere(worldPos,baseScale){
  const group=new THREE.Group();group.position.copy(worldPos);scene.add(group);
  const sphereMat=new THREE.MeshStandardMaterial({color:0xffffff,metalness:0.10,roughness:0.08,transparent:true,opacity:0.66,depthWrite:false,emissive:new THREE.Color(0x070707),emissiveIntensity:0.45});
  const mesh=new THREE.Mesh(new THREE.SphereGeometry(1,128,64),sphereMat);mesh.scale.setScalar(0.001);mesh.rotation.set(Math.random()*Math.PI*2,Math.random()*Math.PI*2,0);group.add(mesh);
  const innerGlowMat=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0,side:THREE.FrontSide,blending:THREE.AdditiveBlending,depthWrite:false});
  const innerGlow=new THREE.Mesh(new THREE.SphereGeometry(0.78,32,32),innerGlowMat);group.add(innerGlow);
  const hazeMat=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0,side:THREE.BackSide,blending:THREE.AdditiveBlending,depthWrite:false});
  const haze=new THREE.Mesh(new THREE.SphereGeometry(1.42,32,32),hazeMat);group.add(haze);
  const recAuraMat=new THREE.MeshBasicMaterial({color:0xff1a1a,transparent:true,opacity:0,side:THREE.BackSide,blending:THREE.AdditiveBlending,depthWrite:false});
  const recAura=new THREE.Mesh(new THREE.SphereGeometry(1.58,32,32),recAuraMat);group.add(recAura);
  const selMat=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthWrite:false,side:THREE.DoubleSide});
  const selRing=new THREE.Mesh(new THREE.TorusGeometry(1.28,0.016,16,128),selMat);selRing.scale.setScalar(baseScale);group.add(selRing);
  const light=new THREE.PointLight(0xffffff,0,20);light.position.set(0,0,1.5);group.add(light);
  const mkT=(r,tube)=>{const m=new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthWrite:false});const tm=new THREE.Mesh(new THREE.TorusGeometry(r,tube,24,160),m);group.add(tm);return{mesh:tm,mat:m};};
  const tori=[mkT(1.55,.026),mkT(2.00,.015),mkT(1.25,.012)];
  const toriMul=[.78,.42,.58];
  const actionLines=[];
  for(let i=0;i<22;i++){const ang=(i/22)*Math.PI*2+(Math.random()-.5)*.22;const cos=Math.cos(ang),sin=Math.sin(ang);const innerR=1.12,outerMax=innerR+.85+Math.random()*2.2;const buf=new Float32Array([cos*innerR,sin*innerR,0,cos*innerR,sin*innerR,0]);const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(buf,3));const mat=new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:0,blending:THREE.AdditiveBlending,depthWrite:false});group.add(new THREE.Line(geo,mat));actionLines.push({geo,mat,cos,sin,innerR,outerMax});}
  const sgn=()=>Math.random()>.5?1:-1;
  const angVel={x:sgn()*(0.003+Math.random()*.010),y:sgn()*(0.004+Math.random()*.013)};
  const labelDiv=document.createElement('div');labelDiv.className='sphere-label';
  const idSpan=document.createElement('span');idSpan.className='sphere-id';idSpan.textContent='\u2205'+String(entityIdCounter).padStart(2,'0');
  const termSpan=document.createElement('span');termSpan.className='sphere-term';termSpan.textContent='';
  labelDiv.appendChild(idSpan);labelDiv.appendChild(termSpan);labelsEl.appendChild(labelDiv);
  const id=entityIdCounter++;
  const entity={id,group,mesh,sphereMat,innerGlow,innerGlowMat,haze,hazeMat,recAura,recAuraMat,selRing,selMat,light,tori,toriMul,actionLines,baseScale,angVel,birthTime:performance.now(),animState:'APPEAR',selected:false,recording:false,words:[],labelDiv,termSpan};
  mesh.userData.entity=entity;meshList.push(mesh);entities.push(entity);updateNetStats();return entity;
}
function updateEntity(e,now,dt){
  const t=(now-e.birthTime)/1000;
  let rawS;
  if(e.animState==='APPEAR'){rawS=sampleKF(clamp01(t/ANIM_DUR))*e.baseScale;if(t>=ANIM_DUR)e.animState='ALIVE';}else{rawS=e.baseScale;}
  const s=Math.max(rawS,.001);
  e.mesh.scale.setScalar(s);e.innerGlow.scale.setScalar(s);e.haze.scale.setScalar(s);e.recAura.scale.setScalar(s);
  const normS=clamp01(rawS/e.baseScale);
  if(e.recording){const rp=0.5+Math.sin(now*0.013)*0.43;e.recAuraMat.opacity=normS*(0.50+rp*0.40);e.innerGlowMat.opacity=normS*(0.04+rp*0.04);e.hazeMat.opacity=0;e.sphereMat.emissive.setRGB(0.30+rp*0.22,0.01,0.01);e.sphereMat.emissiveIntensity=1.2+rp*0.8;e.light.color.setRGB(1,0.12,0.12);e.light.intensity=normS*(5+rp*4);e.selMat.opacity=0;}
  else if(e.selected){const pulse=0.5+Math.sin(now*0.0055)*0.25;e.innerGlowMat.opacity=normS*(0.055+pulse*0.055);e.hazeMat.opacity=normS*(0.032+pulse*0.028);e.recAuraMat.opacity=0;e.sphereMat.emissive.setScalar(0.15+pulse*0.10);e.sphereMat.emissiveIntensity=1.0+pulse*0.4;e.sphereMat.opacity=0.76;e.light.color.setRGB(1,1,1);e.light.intensity=normS*(4.5+pulse*2.5);e.selMat.opacity=0.26+Math.sin(now*0.004)*0.12;e.selRing.quaternion.copy(camera.quaternion);}
  else{const idle=Math.sin(now*0.0011+e.id*1.4)*0.008;e.innerGlowMat.opacity=0;e.hazeMat.opacity=normS*(0.012+idle);e.recAuraMat.opacity=0;e.sphereMat.emissive.setScalar(0.015);e.sphereMat.emissiveIntensity=0.40;e.sphereMat.opacity=0.64;e.light.color.setRGB(1,1,1);e.light.intensity=normS*(0.8+Math.sin(now*.0018+e.id)*.28);e.selMat.opacity=0;}
  e.angVel.x*=.995;e.angVel.y*=.995;const fl=.0003;if(Math.abs(e.angVel.x)<fl)e.angVel.x=fl*Math.sign(e.angVel.x||1);if(Math.abs(e.angVel.y)<fl)e.angVel.y=fl*Math.sign(e.angVel.y||1);e.mesh.rotation.x+=e.angVel.x;e.mesh.rotation.y+=e.angVel.y;
  [[0],[.07],[.03]].forEach(([d],i)=>{const a=torusAnim(t,d);e.tori[i].mat.opacity=a.op*e.toriMul[i];e.tori[i].mesh.scale.setScalar(a.scale);});
  e.actionLines.forEach((ld,i)=>{const a=lineAnim(t,i);ld.mat.opacity=a.op*.72;const r=ld.innerR+a.outerFrac*(ld.outerMax-ld.innerR);const p=ld.geo.attributes.position;p.setXYZ(1,ld.cos*r,ld.sin*r,0);p.needsUpdate=true;});
  const v=e.group.position.clone().project(camera);
  const sx=(v.x*.5+.5)*window.innerWidth,sy=(-v.y*.5+.5)*window.innerHeight;
  const screenR=(e.baseScale/camRadius)*window.innerHeight*0.66;
  e.labelDiv.style.left=sx+'px';e.labelDiv.style.top=(sy+screenR+10)+'px';e.labelDiv.style.opacity=v.z<1?'1':'0';
  const nc='sphere-label'+(e.recording?' rec':e.selected?' sel':'');if(e.labelDiv.className!==nc)e.labelDiv.className=nc;
}
function addConnection(ea,eb){if(ea===eb)return false;if(connections.some(c=>(c.a===ea&&c.b===eb)||(c.a===eb&&c.b===ea)))return false;const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(new Float32Array(6),3));const mat=new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.20,blending:THREE.AdditiveBlending,depthWrite:false});scene.add(new THREE.Line(geo,mat));connections.push({a:ea,b:eb,geo,mat});updateNetStats();return true;}
function updateConnections(now){connections.forEach(({a,b,geo,mat})=>{const pa=a.group.position,pb=b.group.position;const p=geo.attributes.position;p.setXYZ(0,pa.x,pa.y,pa.z);p.setXYZ(1,pb.x,pb.y,pb.z);p.needsUpdate=true;mat.opacity=0.12+Math.sin(now*.0015+a.id*.9)*.07;});}
function toggleSelect(ent){if(ent.selected){ent.selected=false;selected=selected.filter(e=>e!==ent);}else{if(selected.length>=2){selected[0].selected=false;selected.shift();}ent.selected=true;selected.push(ent);}refreshSelInfo();}
function deselectAll(){selected.forEach(e=>{e.selected=false;});selected=[];refreshSelInfo();}
let spaceDown=false,shiftDown=false,middleDown=false;
let mousedownClient={x:0,y:0},potentialDragEnt=null,isDraggingSphere=false,dragEntity=null;
const _dragPlane=new THREE.Plane(),_dragRc=new THREE.Raycaster(),_clickRc=new THREE.Raycaster();
canvas.addEventListener('wheel',e=>{e.preventDefault();camRadius=Math.max(1.2,Math.min(80,camRadius+e.deltaY*0.01*(shiftDown?.04:.28)));},{passive:false});
canvas.addEventListener('mousedown',e=>{if(e.button===1){middleDown=true;e.preventDefault();}});
window.addEventListener('mouseup',e=>{if(e.button===1)middleDown=false;});
window.addEventListener('mousemove',e=>{const mx=e.movementX,my=e.movementY;if(middleDown&&!spaceDown){const spd=shiftDown?.0018:.007;camTheta-=mx*spd;camPhi=Math.max(.04,Math.min(Math.PI-.04,camPhi-my*spd));}if(spaceDown&&(e.buttons&1)&&!isDraggingSphere){const spd=shiftDown?.003:.014;const right=new THREE.Vector3().setFromMatrixColumn(camera.matrix,0);const up=new THREE.Vector3().setFromMatrixColumn(camera.matrix,1);camTarget.addScaledVector(right,-mx*spd);camTarget.addScaledVector(up,my*spd);}if(potentialDragEnt&&(e.buttons&1)&&!isDraggingSphere){const dx=e.clientX-mousedownClient.x,dy=e.clientY-mousedownClient.y;if(Math.sqrt(dx*dx+dy*dy)>5){isDraggingSphere=true;dragEntity=potentialDragEnt;const cd=new THREE.Vector3();camera.getWorldDirection(cd);_dragPlane.setFromNormalAndCoplanarPoint(cd,dragEntity.group.position);}}if(isDraggingSphere&&dragEntity){_dragRc.setFromCamera(mouseNDC,camera);const hit=new THREE.Vector3();if(_dragRc.ray.intersectPlane(_dragPlane,hit))dragEntity.group.position.copy(hit);}});
canvas.addEventListener('mousedown',e=>{if(e.button!==0)return;mousedownClient={x:e.clientX,y:e.clientY};potentialDragEnt=null;isDraggingSphere=false;const ndc=new THREE.Vector2((e.clientX/window.innerWidth)*2-1,-(e.clientY/window.innerHeight)*2+1);_clickRc.setFromCamera(ndc,camera);const hits=_clickRc.intersectObjects(meshList);if(hits.length)potentialDragEnt=hits[0].object.userData.entity;});
window.addEventListener('mouseup',e=>{if(e.button!==0)return;if(!isDraggingSphere){if(potentialDragEnt&&!spaceDown)toggleSelect(potentialDragEnt);else if(!potentialDragEnt&&!spaceDown)deselectAll();}potentialDragEnt=null;isDraggingSphere=false;dragEntity=null;});
const t1Row=document.getElementById('t1r'),t2Row=document.getElementById('t2r'),t3Row=document.getElementById('t3r'),t4Row=document.getElementById('t4r'),t5Row=document.getElementById('t5r');
const statusEl=document.getElementById('status'),timingWrap=document.getElementById('timing-wrap'),tCursor=document.getElementById('t-cursor');
const sizeWrap=document.getElementById('size-wrap'),sizeFill=document.getElementById('size-fill'),sizeVal=document.getElementById('size-val');
const selInfoEl=document.getElementById('sel-info'),cntS=document.getElementById('cnt-s'),cntC=document.getElementById('cnt-c'),flashEl=document.getElementById('flash');
const setT1=c=>{t1Row.className='trigger-row '+(c||'');};const setT2=c=>{t2Row.className='trigger-row '+(c||'');};const setT3=c=>{t3Row.className='trigger-row '+(c||'');};const setT4=c=>{t4Row.className='trigger-row '+(c||'');};const setT5=c=>{t5Row.className='trigger-row '+(c||'');};
const setStatus=(m,dim=false)=>{statusEl.textContent=m;statusEl.className=dim?'dim':'';};const showTiming=v=>{timingWrap.className=v?'show':'';};const showSize=v=>{sizeWrap.className=v?'show':'';};
function updateNetStats(){cntS.textContent=entities.length;cntC.textContent=connections.length;}
function refreshSelInfo(){if(!selected.length){selInfoEl.style.opacity='0';return;}selInfoEl.style.opacity='0.40';selInfoEl.innerHTML=selected.length===1?'SELECTED \u2205'+String(selected[0].id).padStart(2,'0')+'<br>CLICK ANOTHER TO PAIR':'\u2205'+String(selected[0].id).padStart(2,'0')+' + \u2205'+String(selected[1].id).padStart(2,'0')+'<br>PRESS [3] TO CONNECT';}
function doFlash(){flashEl.style.transition='none';flashEl.style.opacity='0.12';requestAnimationFrame(()=>{flashEl.style.transition='opacity 0.55s ease';flashEl.style.opacity='0';});}
setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');
let state='IDLE',t1RelAt=0,key2PressAt=0;
const WIN_MIN=1.0,WIN_MAX=3.0,SCALE_MIN=.28,SCALE_MAX=2.5,HOLD_MAX=2.0;
const held=new Set();
window.addEventListener('keydown',e=>{
  if(e.code==='Space'){e.preventDefault();spaceDown=true;}if(e.key==='Shift')shiftDown=true;
  if(held.has(e.key))return;held.add(e.key);
  if(e.key==='1'&&state==='IDLE'){state='T1';setT1('active');setT2('');setT3('');setStatus('TRIGGER 01 ACTIVE \u2014 HOLD...');showTiming(false);showSize(false);}
  if(e.key==='2'&&state==='WINDOW'){const we=(performance.now()-t1RelAt)/1000;if(we<WIN_MIN){state='IDLE';setT2('error');setStatus('\u26a0  TOO EARLY \u2014 WINDOW: 1s \u2013 3s');showTiming(false);setTimeout(()=>{setT2('');setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');},1600);}else{state='SIZING';key2PressAt=performance.now();setT2('active');setStatus('HOLD [2] \u2014 SIZE \u2191 \u2014 RELEASE TO APPEAR');showTiming(false);showSize(true);}}
  if(e.key==='3'){if(selected.length===2){const ok=addConnection(selected[0],selected[1]);setT3(ok?'success':'error');setStatus(ok?'\u2205\u2205 EDGE \u2014 '+connections.length+' TOTAL':'\u26a0  ALREADY CONNECTED');deselectAll();setTimeout(()=>{setT3('');if(state==='IDLE')setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');},1400);}else{setT3('error');setStatus('\u26a0  SELECT 2 SPHERES FIRST');setTimeout(()=>{setT3('');if(state==='IDLE')setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');},900);}}
  if(e.key==='4'){const tgt=selected[0]||null;if(!tgt){setT4('error');setStatus('\u26a0  SELECT A SPHERE FIRST');setTimeout(()=>{setT4('');},900);return;}startRecording(tgt);}
  if(e.key==='5'){const tgt=selected[0]||null;if(!tgt){setT5('error');setStatus('\u26a0  SELECT A SPHERE FIRST');setTimeout(()=>{setT5('');},900);return;}if(!isPlayingWords){setT5('active');setStatus('\u25b6  PLAYING WORDS');startWordPlay(tgt);}}
});
window.addEventListener('keyup',e=>{
  if(e.code==='Space')spaceDown=false;if(e.key==='Shift')shiftDown=false;held.delete(e.key);
  if(e.key==='1'&&state==='T1'){state='WINDOW';t1RelAt=performance.now();setT1('');setStatus('WINDOW OPEN \u2014 PRESS [2] IN VALID ZONE');showTiming(true);}
  if(e.key==='2'&&state==='SIZING'){const holdDur=(performance.now()-key2PressAt)/1000;const baseScale=lerp(SCALE_MIN,SCALE_MAX,clamp01(holdDur/HOLD_MAX));_dragRc.setFromCamera(mouseNDC,camera);const cd=new THREE.Vector3();camera.getWorldDirection(cd);const sp=new THREE.Plane().setFromNormalAndCoplanarPoint(cd,camTarget);const pos=new THREE.Vector3();_dragRc.ray.intersectPlane(sp,pos);const ent=spawnSphere(pos,baseScale);state='IDLE';setT2('success');setStatus('\u2205'+String(ent.id).padStart(2,'0')+' SPAWNED \u2014 \u2205 '+baseScale.toFixed(2)+' \u2014 HOLD [1] AGAIN');showSize(false);doFlash();setTimeout(()=>{setT2('');if(state==='IDLE')setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');},2000);}
  if(e.key==='4'&&isRecording)stopRecording();
  if(e.key==='5'&&isPlayingWords){setT5('');stopWordPlay();if(state==='IDLE')setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');}
});
let prevNow=performance.now();
function animate(){requestAnimationFrame(animate);const now=performance.now();const dt=Math.min((now-prevNow)/1000,.05);prevNow=now;applyCam();
  if(state==='WINDOW'){const we=(now-t1RelAt)/1000;tCursor.style.left=(clamp01(we/WIN_MAX)*100).toFixed(2)+'%';tCursor.style.background=we<WIN_MIN?'#555':'#fff';if(we>=WIN_MAX){state='IDLE';showTiming(false);setT2('error');setStatus('\u2715  WINDOW CLOSED');setTimeout(()=>{setT2('');setStatus('HOLD [1] TO ACTIVATE VOCAL TRIGGER');},1600);}}
  if(state==='SIZING'){const pct=clamp01((now-key2PressAt)/1000/HOLD_MAX);sizeFill.style.width=(pct*100).toFixed(1)+'%';sizeVal.textContent='\u2205 '+lerp(SCALE_MIN,SCALE_MAX,pct).toFixed(2);}
  entities.forEach(e=>updateEntity(e,now,dt));updateConnections(now);updateWordDisplay();renderer.render(scene,camera);}
animate();
</script>
</body>
</html>"""

# How to Push This Repository to GitHub

## Step 1 — Create the repository on GitHub

1. Go to https://github.com/new
2. Set **Repository name** to: `nxs-sphere-network`
3. Set **Description** to: `Browser-based 3D concept-network environment for transdisciplinary knowledge ecology research`
4. Set visibility: **Public** (recommended for open research) or Private
5. **Do NOT** initialise with README, .gitignore, or licence — the repo already has these
6. Click **Create repository**

GitHub will show you a page with setup instructions. Keep it open.

---

## Step 2 — Initialise and push from your machine

Open a terminal, navigate to this folder, and run:

```bash
cd /path/to/nxs-sphere-network

git init
git add .
git commit -m "Initial commit: NXS+ Sphere Network — full repository structure"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nxs-sphere-network.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 3 — Add repository metadata on GitHub

After pushing, on the repository page:

1. Click the ⚙️ gear icon next to **About** (top-right of the repo)
2. Add **Website** if you have a project page
3. Add **Topics**:
   ```
   knowledge-graph  multi-agent  three-js  transdisciplinary  cultural-ai
   research-tool  obsidian  whisper  webgl  digital-humanities
   ```
4. Check **Releases**, **Packages**, and **Environments** as appropriate

---

## Step 4 — Recommended: add your nxs-plus.html

Place your current `nxs-plus.html` file into `src/nxs-plus.html` and commit:

```bash
cp /path/to/your/nxs-plus.html src/nxs-plus.html
git add src/nxs-plus.html
git commit -m "Add NXS+ browser application"
git push
```

---

## Step 5 — Optional: enable GitHub Pages

To host the app directly from the repo (no server needed):

1. Go to **Settings → Pages**
2. Source: **Deploy from a branch**
3. Branch: `main`, folder: `/src`
4. Click **Save**

Your app will be live at: `https://YOUR_USERNAME.github.io/nxs-sphere-network/nxs-plus.html`

---

## Repository checklist

- [ ] `src/nxs-plus.html` — main application file added
- [ ] `README.md` — ✅ included
- [ ] `docs/` — ✅ all 6 documentation files included
- [ ] `examples/demo-vault.json` — ✅ included
- [ ] `src/server/whisper_server.py` — ✅ included
- [ ] `.github/CONTRIBUTING.md` — ✅ included
- [ ] `.github/ISSUE_TEMPLATE/` — ✅ 2 templates included
- [ ] `LICENSE` — ✅ MIT included
- [ ] `.gitignore` — ✅ included
- [ ] GitHub Topics added
- [ ] Repository description set

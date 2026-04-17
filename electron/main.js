const { app, BrowserWindow, Menu, shell, dialog, ipcMain } = require('electron')
const path  = require('path')
const fs    = require('fs')
const http  = require('http')
const url   = require('url')

let win = null

// ── Serve the HTML file as a local server (avoids file:// CORS issues) ──
function startLocalServer(htmlPath) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const parsed = url.parse(req.url)
      if (parsed.pathname === '/' || parsed.pathname === '/index.html') {
        fs.readFile(htmlPath, (err, data) => {
          if (err) { res.writeHead(404); res.end('Not found'); return }
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' })
          res.end(data)
        })
      } else {
        res.writeHead(404); res.end()
      }
    })
    server.listen(0, '127.0.0.1', () => {
      const port = server.address().port
      resolve({ server, port })
    })
  })
}

async function createWindow() {
  const htmlPath = path.join(__dirname, 'index.html')

  // Start mini local server so fetch/localStorage work correctly
  const { port } = await startLocalServer(htmlPath)

  win = new BrowserWindow({
    width:  1440,
    height: 900,
    minWidth:  900,
    minHeight: 600,
    backgroundColor: '#000000',
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
    },
    icon: path.join(__dirname, 'assets', 'icon.png'),
    title: '∅ NXS+ Sphere Network',
  })

  win.loadURL(`http://127.0.0.1:${port}`)

  // Open DevTools with Cmd/Ctrl+Shift+I
  win.webContents.on('before-input-event', (event, input) => {
    if (input.type === 'keyDown' && input.key === 'I'
        && input.shift && (input.control || input.meta)) {
      win.webContents.openDevTools()
    }
  })

  // Open external links in default browser
  win.webContents.setWindowOpenHandler(({ url: u }) => {
    if (u.startsWith('http')) shell.openExternal(u)
    return { action: 'deny' }
  })

  win.on('closed', () => { win = null })
}

// ── Application menu ──────────────────────────────────────────────────────────
function buildMenu() {
  const template = [
    ...(process.platform === 'darwin' ? [{
      label: app.name,
      submenu: [
        { role: 'about' },
        { type: 'separator' },
        { role: 'services' },
        { type: 'separator' },
        { role: 'hide' },
        { role: 'hideOthers' },
        { role: 'unhide' },
        { type: 'separator' },
        { role: 'quit' },
      ],
    }] : []),
    {
      label: 'File',
      submenu: [
        process.platform === 'darwin' ? { role: 'close' } : { role: 'quit' }
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
      ],
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About NXS+',
          click: () => {
            dialog.showMessageBox(win, {
              type: 'info',
              title: '∅ NXS+ Sphere Network',
              message: '∅ NXS+ Sphere Network',
              detail: 'CognitiveNexus Research Practice\nIannis Bardakos\n\nA 3D concept network for transdisciplinary creative research.',
              buttons: ['OK'],
            })
          }
        },
        { type: 'separator' },
        {
          label: 'Open DevTools',
          accelerator: process.platform === 'darwin' ? 'Cmd+Shift+I' : 'Ctrl+Shift+I',
          click: () => win && win.webContents.openDevTools(),
        },
      ],
    },
  ]
  Menu.setApplicationMenu(Menu.buildFromTemplate(template))
}

app.whenReady().then(() => {
  buildMenu()
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

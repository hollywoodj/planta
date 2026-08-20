const { app, BrowserWindow, Menu, shell, dialog, session } = require("electron");
const path = require("path");
const fs = require("fs");
const http = require("http");
const net = require("net");
const { spawn } = require("child_process");

const APP_NAME = "Planta";
const DEFAULT_PORT = 8742;

let mainWindow = null;
let serverProcess = null;
let serverPort = DEFAULT_PORT;

function packagedRoot() {
  return process.resourcesPath;
}

function projectRoot() {
  return path.join(__dirname, "..");
}

function resolvePython(runtime) {
  const candidates =
    process.platform === "win32"
      ? [path.join(runtime, "python.exe"), path.join(runtime, "bin", "python.exe")]
      : [
          path.join(runtime, "bin", "python3"),
          path.join(runtime, "bin", "python3.12"),
          path.join(runtime, "bin", "python"),
        ];
  return candidates.find((candidate) => fs.existsSync(candidate)) ?? candidates[0];
}

function pythonBin() {
  if (app.isPackaged) {
    return resolvePython(path.join(packagedRoot(), "python"));
  }
  const bundled = resolvePython(path.join(projectRoot(), "python-runtime"));
  if (fs.existsSync(bundled)) return bundled;
  return process.platform === "win32" ? "python" : "python3";
}

function backendDir() {
  return app.isPackaged ? path.join(packagedRoot(), "backend") : path.join(projectRoot(), "backend");
}

function staticDir() {
  return app.isPackaged
    ? path.join(packagedRoot(), "frontend", "dist")
    : path.join(projectRoot(), "frontend", "dist");
}

function findFreePort(preferred = DEFAULT_PORT) {
  const tryListen = (port) =>
    new Promise((resolve, reject) => {
      const server = net.createServer();
      server.unref();
      server.once("error", reject);
      server.listen(port, "127.0.0.1", () => {
        const address = server.address();
        const resolved = typeof address === "object" && address ? address.port : port;
        server.close((err) => (err ? reject(err) : resolve(resolved)));
      });
    });
  return tryListen(preferred).catch(() => tryListen(0));
}

function waitForHealth(port, attempts = 80) {
  return new Promise((resolve, reject) => {
    let n = 0;
    const tick = () => {
      const req = http.get(`http://127.0.0.1:${port}/api/health`, (res) => {
        res.resume();
        if (res.statusCode === 200) resolve();
        else if (++n >= attempts) reject(new Error("Server health check failed"));
        else setTimeout(tick, 250);
      });
      req.on("error", () => {
        if (++n >= attempts) reject(new Error("Planta API did not start"));
        else setTimeout(tick, 250);
      });
      req.setTimeout(800, () => {
        req.destroy();
        if (++n >= attempts) reject(new Error("Planta API did not start"));
        else setTimeout(tick, 250);
      });
    };
    tick();
  });
}

function startBackend() {
  return new Promise((resolve, reject) => {
    const bin = pythonBin();
    const backend = backendDir();
    const cacheDir = path.join(app.getPath("userData"), "hf-cache");
    fs.mkdirSync(cacheDir, { recursive: true });

    const env = {
      ...process.env,
      PORT: String(serverPort),
      PLANTA_PORT: String(serverPort),
      PLANTA_HOST: "127.0.0.1",
      PLANTA_STATIC_DIR: staticDir(),
      PYTHONPATH: backend,
      HF_HOME: cacheDir,
      TOKENIZERS_PARALLELISM: "false",
      PYTHONUNBUFFERED: "1",
    };

    serverProcess = spawn(bin, ["-m", "planta"], {
      env,
      stdio: "pipe",
      cwd: backend,
      windowsHide: true,
    });

    serverProcess.stdout?.on("data", (chunk) => process.stdout.write(`[planta-api] ${chunk}`));
    serverProcess.stderr?.on("data", (chunk) => process.stderr.write(`[planta-api] ${chunk}`));
    serverProcess.on("error", reject);
    serverProcess.on("exit", (code) => {
      if (code && code !== 0) console.error(`${APP_NAME} API exited with code ${code}`);
    });

    waitForHealth(serverPort).then(resolve).catch(reject);
  });
}

function stopBackend() {
  if (serverProcess && !serverProcess.killed) {
    if (process.platform === "win32" && serverProcess.pid) {
      spawn("taskkill", ["/pid", String(serverProcess.pid), "/f", "/t"]);
    } else {
      serverProcess.kill("SIGTERM");
    }
    serverProcess = null;
  }
}

function buildMenu() {
  const template = [
    ...(process.platform === "darwin"
      ? [
          {
            label: APP_NAME,
            submenu: [
              { role: "about" },
              { type: "separator" },
              { role: "services" },
              { type: "separator" },
              { role: "hide" },
              { role: "hideOthers" },
              { role: "unhide" },
              { type: "separator" },
              { role: "quit" },
            ],
          },
        ]
      : []),
    {
      label: "File",
      submenu: [
        {
          label: "Scan a leaf",
          accelerator: "CmdOrCtrl+N",
          click: () => mainWindow?.webContents.send("menu-command", { type: "scan" }),
        },
        { type: "separator" },
        { role: process.platform === "darwin" ? "close" : "quit" },
      ],
    },
    { role: "editMenu" },
    {
      label: "View",
      submenu: [
        { role: "reload" },
        { role: "toggleDevTools" },
        { type: "separator" },
        { role: "resetZoom" },
        { role: "zoomIn" },
        { role: "zoomOut" },
        { type: "separator" },
        { role: "togglefullscreen" },
      ],
    },
    { role: "windowMenu" },
    {
      label: "Help",
      submenu: [
        {
          label: "PlantVillage paper",
          click: () => shell.openExternal("https://arxiv.org/abs/1511.08060"),
        },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1180,
    height: 820,
    minWidth: 860,
    minHeight: 640,
    title: APP_NAME,
    backgroundColor: "#143326",
    show: false,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  mainWindow.once("ready-to-show", () => mainWindow.show());
  mainWindow.webContents.setWindowOpenHandler(({ url: next }) => {
    shell.openExternal(next);
    return { action: "deny" };
  });
  mainWindow.webContents.on("will-navigate", (event, next) => {
    if (next.startsWith("http://127.0.0.1:") || next.startsWith("http://localhost:")) return;
    event.preventDefault();
    shell.openExternal(next);
  });

  await mainWindow.loadFile(path.join(__dirname, "loading.html"));
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

async function loadApp(url) {
  if (!mainWindow) await createWindow();
  await mainWindow.loadURL(url);
}

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  app.whenReady().then(async () => {
    session.defaultSession.setPermissionRequestHandler((_contents, permission, callback) => {
      callback(permission === "media" || permission === "mediaKeySystem");
    });
    buildMenu();
    try {
      await createWindow();
      if (process.env.ELECTRON_START_URL) {
        await loadApp(process.env.ELECTRON_START_URL);
      } else {
        serverPort = await findFreePort(DEFAULT_PORT);
        await startBackend();
        await loadApp(`http://127.0.0.1:${serverPort}/`);
      }
    } catch (err) {
      dialog.showErrorBox(
        `${APP_NAME} failed to start`,
        err instanceof Error ? err.message : String(err),
      );
      app.quit();
    }
  });

  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") app.quit();
  });

  app.on("activate", async () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      const url = process.env.ELECTRON_START_URL || `http://127.0.0.1:${serverPort}/`;
      await createWindow();
      await loadApp(url);
    }
  });

  app.on("before-quit", () => stopBackend());
}

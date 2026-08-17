const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("plantaDesktop", {
  platform: process.platform,
  onMenuCommand: (callback) => {
    const listener = (_event, command) => callback(command);
    ipcRenderer.on("menu-command", listener);
    return () => ipcRenderer.removeListener("menu-command", listener);
  },
});

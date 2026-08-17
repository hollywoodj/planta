import { createWriteStream, existsSync } from "node:fs";
import { chmod, cp, mkdir, rm } from "node:fs/promises";
import { get } from "node:https";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { pipeline } from "node:stream/promises";
import { execFileSync } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const RUNTIME = join(ROOT, "python-runtime");
const STANDALONE_TAG = "20260814";
const CPYTHON = "3.12.14";

function assetName() {
  const { platform, arch } = process;
  if (platform === "darwin" && arch === "arm64") {
    return `cpython-${CPYTHON}+${STANDALONE_TAG}-aarch64-apple-darwin-install_only.tar.gz`;
  }
  if (platform === "darwin" && arch === "x64") {
    return `cpython-${CPYTHON}+${STANDALONE_TAG}-x86_64-apple-darwin-install_only.tar.gz`;
  }
  if (platform === "win32") {
    return `cpython-${CPYTHON}+${STANDALONE_TAG}-x86_64-pc-windows-msvc-install_only.tar.gz`;
  }
  if (platform === "linux" && arch === "arm64") {
    return `cpython-${CPYTHON}+${STANDALONE_TAG}-aarch64-unknown-linux-gnu-install_only.tar.gz`;
  }
  return `cpython-${CPYTHON}+${STANDALONE_TAG}-x86_64-unknown-linux-gnu-install_only.tar.gz`;
}

function pythonBin() {
  return process.platform === "win32"
    ? join(RUNTIME, "python.exe")
    : join(RUNTIME, "bin", "python3");
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const request = (current) => {
      get(current, (response) => {
        const location = response.headers.location;
        if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && location) {
          request(location);
          return;
        }
        if (response.statusCode !== 200) {
          reject(new Error(`Download failed: ${response.statusCode} ${url}`));
          return;
        }
        pipeline(response, createWriteStream(dest)).then(resolve).catch(reject);
      }).on("error", reject);
    };
    request(url);
  });
}

function pip(bin, args) {
  execFileSync(bin, ["-m", "pip", ...args], { stdio: "inherit", cwd: ROOT });
}

async function main() {
  if (existsSync(pythonBin()) && !process.env.FORCE_BUNDLE) {
    console.log(`python-runtime already exists at ${RUNTIME}`);
    return;
  }

  await rm(RUNTIME, { recursive: true, force: true });
  const archive = join(tmpdir(), assetName());
  const url = `https://github.com/astral-sh/python-build-standalone/releases/download/${STANDALONE_TAG}/${assetName()}`;
  console.log(`Downloading ${url}`);
  await download(url, archive);

  const extractDir = join(tmpdir(), `planta-python-${process.pid}`);
  await rm(extractDir, { recursive: true, force: true });
  await mkdir(extractDir, { recursive: true });
  execFileSync("tar", ["-xzf", archive, "-C", extractDir], { stdio: "inherit" });

  const unpacked = join(extractDir, "python");
  if (!existsSync(unpacked)) {
    throw new Error(`Unexpected python-build-standalone layout in ${extractDir}`);
  }
  await cp(unpacked, RUNTIME, { recursive: true });
  await rm(extractDir, { recursive: true, force: true });

  const bin = pythonBin();
  if (process.platform !== "win32") await chmod(bin, 0o755);

  pip(bin, ["install", "-U", "pip"]);
  pip(bin, ["install", "-r", join(ROOT, "backend", "requirements.txt")]);
  if (process.platform === "linux") {
    pip(bin, [
      "install",
      "torch==2.8.0",
      "--index-url",
      "https://download.pytorch.org/whl/cpu",
    ]);
  } else {
    pip(bin, ["install", "torch==2.8.0"]);
  }
  console.log("Bundled Python runtime is ready.");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

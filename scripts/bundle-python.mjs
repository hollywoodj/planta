import { createWriteStream, existsSync, readdirSync } from "node:fs";
import { mkdir, rm, stat } from "node:fs/promises";
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

export function assetName(platform = process.platform, arch = process.arch) {
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

export function pythonBin(runtime = RUNTIME, platform = process.platform) {
  const candidates =
    platform === "win32"
      ? [join(runtime, "python.exe"), join(runtime, "bin", "python.exe")]
      : [
          join(runtime, "bin", "python3"),
          join(runtime, "bin", "python3.12"),
          join(runtime, "bin", "python"),
        ];
  return candidates.find((path) => existsSync(path)) ?? candidates[0];
}

function download(url, dest) {
  return new Promise((resolve, reject) => {
    const request = (current) => {
      get(current, (response) => {
        const location = response.headers.location;
        if (response.statusCode && response.statusCode >= 300 && response.statusCode < 400 && location) {
          request(new URL(location, current).toString());
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

function describeRuntime() {
  const binDir = join(RUNTIME, "bin");
  if (!existsSync(binDir)) {
    const top = existsSync(RUNTIME) ? readdirSync(RUNTIME).join(", ") : "(missing)";
    return `python-runtime contents: ${top}`;
  }
  return `python-runtime/bin: ${readdirSync(binDir).join(", ")}`;
}

async function main() {
  if (existsSync(pythonBin()) && !process.env.FORCE_BUNDLE) {
    console.log(`python-runtime already exists at ${RUNTIME}`);
    return;
  }

  await rm(RUNTIME, { recursive: true, force: true });
  await mkdir(RUNTIME, { recursive: true });

  const name = assetName();
  const archive = join(tmpdir(), name.replaceAll("+", "_"));
  const url = `https://github.com/astral-sh/python-build-standalone/releases/download/${STANDALONE_TAG}/${name.replaceAll("+", "%2B")}`;
  console.log(`Downloading ${url}`);
  await download(url, archive);

  const downloaded = await stat(archive);
  if (downloaded.size < 1_000_000) {
    throw new Error(`Standalone Python download is too small (${downloaded.size} bytes)`);
  }

  // tar preserves python3 -> python3.12 symlinks; Node fs.cp on macOS does not.
  execFileSync("tar", ["-xzf", archive, "-C", RUNTIME, "--strip-components=1"], {
    stdio: "inherit",
  });

  const bin = pythonBin();
  if (!existsSync(bin)) {
    throw new Error(`Python binary missing at ${bin}. ${describeRuntime()}`);
  }

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

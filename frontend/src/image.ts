function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => resolve(image)
    image.onerror = () => reject(new Error("Could not read that image"))
    image.src = src
  })
}

export async function fileToJpeg(
  file: Blob,
  maxEdge = 1280,
  quality = 0.88,
): Promise<{ blob: Blob; dataUrl: string }> {
  const src = URL.createObjectURL(file)
  try {
    const image = await loadImage(src)
    const scale = Math.min(1, maxEdge / Math.max(image.width, image.height))
    const width = Math.max(1, Math.round(image.width * scale))
    const height = Math.max(1, Math.round(image.height * scale))
    const canvas = document.createElement("canvas")
    canvas.width = width
    canvas.height = height
    const ctx = canvas.getContext("2d")
    if (!ctx) throw new Error("Canvas is not available")
    ctx.drawImage(image, 0, 0, width, height)
    const dataUrl = canvas.toDataURL("image/jpeg", quality)
    const blob = await new Promise<Blob>((resolve, reject) => {
      canvas.toBlob(
        (value) => (value ? resolve(value) : reject(new Error("Could not compress image"))),
        "image/jpeg",
        quality,
      )
    })
    return { blob, dataUrl }
  } finally {
    URL.revokeObjectURL(src)
  }
}

export function captureFrame(video: HTMLVideoElement, maxEdge = 1280): Promise<Blob> {
  const scale = Math.min(1, maxEdge / Math.max(video.videoWidth, video.videoHeight))
  const width = Math.max(1, Math.round(video.videoWidth * scale))
  const height = Math.max(1, Math.round(video.videoHeight * scale))
  const canvas = document.createElement("canvas")
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext("2d")
  if (!ctx) return Promise.reject(new Error("Canvas is not available"))
  ctx.drawImage(video, 0, 0, width, height)
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (value) => (value ? resolve(value) : reject(new Error("Could not capture frame"))),
      "image/jpeg",
      0.9,
    )
  })
}

export function uid(): string {
  return crypto.randomUUID?.() ?? `scan-${Date.now()}`
}

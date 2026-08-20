function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const image = new Image()
    image.onload = () => resolve(image)
    image.onerror = () => reject(new Error("Could not read that image"))
    image.src = src
  })
}

async function drawToJpeg(
  source: CanvasImageSource,
  sourceWidth: number,
  sourceHeight: number,
  maxEdge: number,
  quality: number,
): Promise<{ blob: Blob; dataUrl: string }> {
  const scale = Math.min(1, maxEdge / Math.max(sourceWidth, sourceHeight, 1))
  const width = Math.max(1, Math.round(sourceWidth * scale))
  const height = Math.max(1, Math.round(sourceHeight * scale))
  const canvas = document.createElement("canvas")
  canvas.width = width
  canvas.height = height
  const ctx = canvas.getContext("2d")
  if (!ctx) throw new Error("Canvas is not available")
  ctx.drawImage(source, 0, 0, width, height)
  const dataUrl = canvas.toDataURL("image/jpeg", quality)
  const blob = await new Promise<Blob>((resolve, reject) => {
    canvas.toBlob(
      (value) => (value ? resolve(value) : reject(new Error("Could not compress image"))),
      "image/jpeg",
      quality,
    )
  })
  return { blob, dataUrl }
}

export async function fileToJpeg(
  file: Blob,
  maxEdge = 1280,
  quality = 0.88,
): Promise<{ blob: Blob; dataUrl: string }> {
  try {
    const bitmap = await createImageBitmap(file, { imageOrientation: "from-image" })
    try {
      return await drawToJpeg(bitmap, bitmap.width, bitmap.height, maxEdge, quality)
    } finally {
      bitmap.close()
    }
  } catch {
    const src = URL.createObjectURL(file)
    try {
      const image = await loadImage(src)
      return await drawToJpeg(image, image.width, image.height, maxEdge, quality)
    } finally {
      URL.revokeObjectURL(src)
    }
  }
}

export function captureFrame(video: HTMLVideoElement, maxEdge = 1280): Promise<Blob> {
  if (!video.videoWidth || !video.videoHeight) {
    return Promise.reject(new Error("Camera is not ready yet"))
  }
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

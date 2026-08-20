import type { HistoryItem } from "./types"

const KEY = "planta.history.v1"
const LIMIT = 24

export function loadHistory(): HistoryItem[] {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw) as HistoryItem[]
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function saveHistory(items: HistoryItem[]): HistoryItem[] {
  let next = items.slice(0, LIMIT)
  for (let attempt = 0; attempt < 10; attempt += 1) {
    try {
      localStorage.setItem(KEY, JSON.stringify(next))
      return next
    } catch {
      const oldestWithPhoto = [...next].reverse().find((row) => row.dataUrl)
      if (oldestWithPhoto) {
        next = next.map((row) => (row.id === oldestWithPhoto.id ? { ...row, dataUrl: "" } : row))
        continue
      }
      if (next.length === 0) break
      next = next.slice(0, Math.max(0, next.length - 4))
    }
  }
  try {
    localStorage.removeItem(KEY)
  } catch {
    /* ignore */
  }
  return []
}

export function pushHistory(item: HistoryItem): HistoryItem[] {
  const next = [item, ...loadHistory().filter((row) => row.id !== item.id)]
  return saveHistory(next)
}

export function clearHistory(): void {
  localStorage.removeItem(KEY)
}

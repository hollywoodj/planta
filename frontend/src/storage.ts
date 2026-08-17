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

export function saveHistory(items: HistoryItem[]): void {
  localStorage.setItem(KEY, JSON.stringify(items.slice(0, LIMIT)))
}

export function pushHistory(item: HistoryItem): HistoryItem[] {
  const next = [item, ...loadHistory().filter((row) => row.id !== item.id)].slice(0, LIMIT)
  saveHistory(next)
  return next
}

export function clearHistory(): void {
  localStorage.removeItem(KEY)
}

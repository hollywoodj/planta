import type { HistoryItem } from "./types"

type Props = {
  items: HistoryItem[]
  onOpen: (item: HistoryItem) => void
  onClear: () => void
}

export function History({ items, onOpen, onClear }: Props) {
  return (
    <section className="panel">
      <p className="eyebrow">Your scans</p>
      <h1>Recent leaves</h1>
      {items.length === 0 ? (
        <p className="lede">Nothing here yet. Scan a leaf and it will land in this notebook.</p>
      ) : (
        <>
          <button type="button" className="text-btn" onClick={onClear}>
            Clear history
          </button>
          <div className="history-list">
            {items.map((item) => (
              <button key={item.id} type="button" className="history-row" onClick={() => onOpen(item)}>
                {item.dataUrl ? (
                  <img src={item.dataUrl} alt="" />
                ) : (
                  <span className="history-placeholder" aria-hidden="true" />
                )}
                <span>
                  <strong>
                    {item.crop} · {item.name}
                  </strong>
                  <small>
                    {new Date(item.createdAt).toLocaleString()} · {Math.round(item.confidence * 100)}%
                  </small>
                </span>
              </button>
            ))}
          </div>
        </>
      )}
    </section>
  )
}

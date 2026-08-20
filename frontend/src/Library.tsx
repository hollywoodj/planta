import { useMemo, useState } from "react"
import type { CropSummary, Disease } from "./types"

type Props = {
  diseases: Disease[]
  crops: CropSummary[]
  selectedId: string | null
  onSelect: (id: string | null) => void
}

const KIND_LABEL = {
  organic: "Organic",
  cultural: "Garden practice",
  chemical: "Conventional",
} as const

export function Library({ diseases, crops, selectedId, onSelect }: Props) {
  const [query, setQuery] = useState("")
  const [crop, setCrop] = useState("All")
  const selected = diseases.find((row) => row.id === selectedId) ?? null

  const filtered = useMemo(() => {
    const needle = query.trim().toLowerCase()
    return diseases.filter((row) => {
      if (crop !== "All" && row.crop !== crop) return false
      if (!needle) return true
      const hay = `${row.crop} ${row.name} ${row.scientific_name ?? ""} ${row.summary} ${row.symptoms.join(" ")}`.toLowerCase()
      return hay.includes(needle)
    })
  }, [diseases, query, crop])

  if (selected) {
    const similar = selected.similar
      .map((id) => diseases.find((row) => row.id === id))
      .filter((row): row is Disease => Boolean(row))
    return (
      <section className="panel library-detail">
        <button type="button" className="text-btn" onClick={() => onSelect(null)}>
          ← All ailments
        </button>
        <p className="eyebrow">{selected.crop}</p>
        <h1>{selected.name}</h1>
        <div className="meta-row">
          <span className={`pill severity-${selected.severity}`}>{selected.severity}</span>
          <span className="pill muted">{selected.pathogen_type}</span>
          {selected.contagious && <span className="pill warn">Spreads</span>}
        </div>
        {selected.scientific_name && (
          <p className="scientific">
            <em>{selected.scientific_name}</em>
          </p>
        )}
        <p className="summary">{selected.summary}</p>
        <h2>Symptoms</h2>
        <ul>
          {selected.symptoms.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <h2>Why it happens</h2>
        <ul>
          {selected.causes.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <h2>Treatment</h2>
        {selected.treatments.map((treatment) => (
          <div key={treatment.title} className="treatment">
            <span className={`kind kind-${treatment.kind}`}>{KIND_LABEL[treatment.kind]}</span>
            <h3>{treatment.title}</h3>
            <p>{treatment.details}</p>
          </div>
        ))}
        <h2>Prevention</h2>
        <ul>
          {selected.prevention.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        {similar.length > 0 && (
          <>
            <h2>Easy to confuse with</h2>
            <div className="chip-row">
              {similar.map((row) => (
                <button key={row.id} type="button" className="chip" onClick={() => onSelect(row.id)}>
                  {row.name}
                </button>
              ))}
            </div>
          </>
        )}
      </section>
    )
  }

  return (
    <section className="panel">
      <p className="eyebrow">Field guide</p>
      <h1>Every crop and ailment Planta can name</h1>
      <p className="lede">
        Trained on PlantVillage: apple, blueberry, cherry, corn, grape, orange, peach, pepper,
        potato, raspberry, soybean, squash, strawberry, and tomato.
      </p>
      <div className="filters">
        <input
          type="search"
          placeholder="Search scab, blight, mites…"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <select value={crop} onChange={(event) => setCrop(event.target.value)} aria-label="Filter by crop">
          <option>All</option>
          {crops.map((row) => (
            <option key={row.name}>{row.name}</option>
          ))}
        </select>
      </div>
      {filtered.length === 0 ? (
        <p className="lede">No ailments match that search. Try a crop name or a symptom like “blight”.</p>
      ) : (
        <div className="library-grid">
          {filtered.map((row) => (
            <button key={row.id} type="button" className="lib-card" onClick={() => onSelect(row.id)}>
              <span className="lib-crop">{row.crop}</span>
              <strong>{row.name}</strong>
              <span className={`pill severity-${row.severity}`}>{row.severity}</span>
            </button>
          ))}
        </div>
      )}
    </section>
  )
}

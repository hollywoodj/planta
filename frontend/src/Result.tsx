import type { Disease, ScanResult } from "./types"

type Props = {
  result: ScanResult
  preview: string
  diseases: Disease[]
  onRescan: () => void
  onOpenDisease: (id: string) => void
}

const KIND_LABEL = {
  organic: "Organic",
  cultural: "Garden practice",
  chemical: "Conventional",
} as const

export function Result({ result, preview, diseases, onRescan, onOpenDisease }: Props) {
  const disease = result.top.disease
  const similar = (disease?.similar ?? [])
    .map((id) => diseases.find((row) => row.id === id))
    .filter((row): row is Disease => Boolean(row))

  return (
    <section className="panel result">
      <div className="result-hero">
        <img src={preview} alt="" className="result-photo" />
        <div className="result-headline">
          <p className="eyebrow">{result.top.crop}</p>
          <h1>{result.top.name}</h1>
          <div className="meta-row">
            <span className={`pill severity-${disease?.severity ?? "none"}`}>
              {result.healthy ? "Healthy" : (disease?.severity ?? "unknown")}
            </span>
            {disease && !result.healthy && (
              <span className="pill muted">{disease.pathogen_type}</span>
            )}
            {disease?.contagious && <span className="pill warn">Spreads</span>}
          </div>
          <p className="lede">{result.note}</p>
          <Confidence value={result.top.confidence} band={result.confidence_band} />
        </div>
      </div>

      {disease && (
        <>
          <p className="summary">{disease.summary}</p>
          {disease.scientific_name && (
            <p className="scientific">
              <em>{disease.scientific_name}</em>
            </p>
          )}

          <div className="split">
            <article>
              <h2>Symptoms to confirm</h2>
              <ul>
                {disease.symptoms.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
              <h2>Why it happens</h2>
              <ul>
                {disease.causes.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
            <article>
              <h2>What to do</h2>
              <div className="treatments">
                {disease.treatments.map((treatment) => (
                  <div key={treatment.title} className="treatment">
                    <span className={`kind kind-${treatment.kind}`}>
                      {KIND_LABEL[treatment.kind]}
                    </span>
                    <h3>{treatment.title}</h3>
                    <p>{treatment.details}</p>
                  </div>
                ))}
              </div>
              <h2>Keep it from coming back</h2>
              <ul>
                {disease.prevention.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </article>
          </div>
        </>
      )}

      {result.alternatives.length > 0 && (
        <div>
          <h2>Other possible matches</h2>
          <div className="alt-grid">
            {result.alternatives.map((alt) => (
              <button
                key={alt.id}
                type="button"
                className="alt-card"
                onClick={() => onOpenDisease(alt.id)}
              >
                <strong>
                  {alt.crop} · {alt.name}
                </strong>
                <span>{Math.round(alt.confidence * 100)}%</span>
              </button>
            ))}
          </div>
        </div>
      )}

      {similar.length > 0 && (
        <div>
          <h2>Easy to confuse with</h2>
          <div className="chip-row">
            {similar.map((row) => (
              <button key={row.id} type="button" className="chip" onClick={() => onOpenDisease(row.id)}>
                {row.name}
              </button>
            ))}
          </div>
        </div>
      )}

      <p className="disclaimer">
        Planta is a screening tool trained on the PlantVillage leaf dataset. It is not a replacement
        for a local agronomist, extension agent, or certified pesticide recommendation. Always read
        product labels and follow your region&apos;s rules.
      </p>

      <button type="button" className="btn primary" onClick={onRescan}>
        Scan another leaf
      </button>
    </section>
  )
}

function Confidence({ value, band }: { value: number; band: string }) {
  const pct = Math.round(value * 100)
  return (
    <div className="confidence">
      <div className="confidence-top">
        <span>Model confidence</span>
        <strong>
          {pct}% · {band}
        </strong>
      </div>
      <div className="bar" aria-hidden="true">
        <span style={{ width: `${pct}%` }} />
      </div>
    </div>
  )
}

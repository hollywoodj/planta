type IconProps = { className?: string }

export function LeafMark({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <path
        d="M26.5 5.5C16 6 7.5 13.2 6 23.5c6.8.6 14.2-2.6 18.7-9.1 1.6 4.2.6 9.1-2.7 13.1 7.2-3.2 10.4-11.4 8.2-19.5-.2-.8-1.2-1.3-2-1.1Z"
        fill="currentColor"
      />
      <path
        d="M11 21.5c4.6-3.4 9.6-8.2 13.2-14"
        stroke="#f3eee4"
        strokeWidth="1.4"
        strokeLinecap="round"
      />
    </svg>
  )
}

export function CameraIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M8 7.5 9.2 5.8A1.5 1.5 0 0 1 10.4 5h3.2a1.5 1.5 0 0 1 1.2.8L16 7.5h2.5A2.5 2.5 0 0 1 21 10v7.5A2.5 2.5 0 0 1 18.5 20h-13A2.5 2.5 0 0 1 3 17.5V10a2.5 2.5 0 0 1 2.5-2.5H8Z"
        stroke="currentColor"
        strokeWidth="1.6"
      />
      <circle cx="12" cy="13.5" r="3.1" stroke="currentColor" strokeWidth="1.6" />
    </svg>
  )
}

export function UploadIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M12 16V7m0 0 3.5 3.5M12 7 8.5 10.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M5 16.5V18a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
    </svg>
  )
}

export function BookIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M5 5.5A2.5 2.5 0 0 1 7.5 3H20v16.5H7.5A2.5 2.5 0 0 0 5 22V5.5Z"
        stroke="currentColor"
        strokeWidth="1.6"
      />
      <path d="M5 19.5h12" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  )
}

export function ClockIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="12" cy="12" r="8" stroke="currentColor" strokeWidth="1.6" />
      <path d="M12 8v4.2L15 15" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
    </svg>
  )
}

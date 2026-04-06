export default function CriticalSignals({ signals }) {
  return (
    <div className="card-tonal" style={{ gridColumn: 'span 4', display: 'flex', flexDirection: 'column' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem' }}>
        <span className="material-symbols-outlined" style={{ color: 'var(--secondary-fixed-dim)' }}>sensors</span>
        <h3 style={{
          fontFamily: 'var(--font-headline)', fontSize: '1.25rem',
          fontWeight: 700, letterSpacing: '-0.01em', color: 'var(--primary)',
        }}>
          Actionable Intelligence
        </h3>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', flex: 1 }}>
        {signals.slice(0, 3).map((signal, i) => (
          <div
            key={signal.id || i}
            className={`signal-item ${signal.severity === 'high' ? 'highlighted' : ''}`}
          >
            <span style={{
              fontSize: '10px', textTransform: 'uppercase', fontWeight: 700,
              color: signal.severity === 'high' ? 'var(--secondary-fixed-dim)' : 'var(--on-surface-variant)',
              display: 'block', marginBottom: '0.25rem', letterSpacing: '0.1em',
            }}>
              {signal.signal_type?.replace('_', ' ') || signal.source}
            </span>
            <p style={{ fontSize: '0.875rem', color: 'var(--on-surface)', lineHeight: 1.4 }}>
              {signal.summary || signal.subject}
            </p>
          </div>
        ))}
      </div>

      <button style={{
        marginTop: '2rem', color: 'var(--on-surface-variant)',
        fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.15em',
        fontWeight: 700, background: 'none', border: 'none',
        display: 'flex', alignItems: 'center', gap: '0.5rem',
        transition: 'color 0.3s', cursor: 'pointer',
      }}>
        Review All Intelligence
        <span className="material-symbols-outlined" style={{ fontSize: '0.875rem' }}>arrow_forward</span>
      </button>
    </div>
  );
}

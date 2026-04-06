export default function StatsRow({ riskCount, signalCount, okrCount }) {
  return (
    <section style={{
      display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
      gap: '3rem', marginBottom: '8rem',
    }}>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <span className="text-stat" style={{ color: 'var(--error)', marginBottom: '0.5rem' }}>
          {riskCount}
        </span>
        <span className="text-label">Risk Flags</span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <span className="text-stat" style={{ color: 'var(--secondary-fixed-dim)', marginBottom: '0.5rem' }}>
          {signalCount}
        </span>
        <span className="text-label">Alpha Signals</span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <span className="text-stat" style={{ color: 'var(--primary)', marginBottom: '0.5rem' }}>
          {okrCount}
        </span>
        <span className="text-label">Strategic OKRs</span>
      </div>
    </section>
  );
}

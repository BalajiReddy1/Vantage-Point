export default function OKRProgress({ okrs }) {
  const getProgressClass = (status) => {
    if (status === 'off_track') return 'danger';
    if (status === 'at_risk') return 'danger';
    return 'aurora';
  };

  return (
    <div className="card-tonal" style={{ gridColumn: 'span 8' }}>
      {/* Aurora mesh overlay */}
      <div style={{
        position: 'absolute', top: 0, right: 0, width: '100%', height: '100%',
        opacity: 0.05, pointerEvents: 'none',
        background: 'linear-gradient(135deg, #d3fbff, #fff2fd)',
        filter: 'blur(48px)',
      }} />

      <div style={{ position: 'relative', zIndex: 1 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '3rem' }}>
          <div>
            <h3 className="text-headline-lg" style={{ marginBottom: '0.5rem' }}>Performance Benchmarks</h3>
            <p style={{ color: 'var(--on-surface-variant)', fontSize: '0.875rem' }}>
              Key results across portfolio entities
            </p>
          </div>
          <span className="material-symbols-outlined" style={{ color: 'var(--on-surface-variant)' }}>trending_up</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          {okrs.map((okr, i) => (
            <div key={okr.id || i}>
              <div style={{
                display: 'flex', justifyContent: 'space-between',
                marginBottom: '0.5rem',
              }}>
                <span className="text-label">{okr.key_result}</span>
                <span className="text-label">{Math.round(okr.progress_pct)}%</span>
              </div>
              <div className="progress-track">
                <div
                  className={`progress-fill ${getProgressClass(okr.status)}`}
                  style={{ width: `${okr.progress_pct}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

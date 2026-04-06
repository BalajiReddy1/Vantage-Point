import { useNavigate } from 'react-router-dom';

export default function RiskLandscape({ risks }) {
  const navigate = useNavigate();

  const getSeverityClass = (severity) => {
    if (severity === 'high') return 'high';
    if (severity === 'medium') return 'medium';
    return 'low';
  };

  return (
    <div className="card-tonal" style={{ gridColumn: '1 / -1' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2.5rem' }}>
        <h3 className="text-headline-lg">Fund Risk Matrix</h3>
        <button className="btn-ghost">Deep Analysis</button>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${Math.min(risks.length, 4)}, 1fr)`,
        gap: '2rem',
      }}>
        {risks.map((risk, i) => (
          <div
            key={risk.id || i}
            style={{ cursor: 'pointer', transition: 'transform 0.3s' }}
            onClick={() => navigate(`/risk/${risk.id || i}`)}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-2px)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
          >
            <div className={`risk-bar ${getSeverityClass(risk.severity)}`} />
            <h4 style={{
              fontSize: '0.875rem', fontWeight: 700,
              color: 'var(--on-surface)', marginBottom: '0.5rem',
            }}>
              {risk.title}
            </h4>
            <p style={{
              fontSize: '0.75rem', color: 'var(--on-surface-variant)',
              lineHeight: 1.6,
            }}>
              {risk.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

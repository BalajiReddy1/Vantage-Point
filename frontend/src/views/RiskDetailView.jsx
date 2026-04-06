import { useParams, useNavigate } from 'react-router-dom';

export default function RiskDetailView({ data }) {
  const { riskId } = useParams();
  const navigate = useNavigate();

  const risks = data?.risks || [];
  const risk = risks.find(r => String(r.id) === riskId) || risks[parseInt(riskId)] || risks[0];

  if (!risk) {
    return (
      <main className="main-content" style={{ textAlign: 'center', paddingTop: '12rem' }}>
        <h2 style={{ color: 'var(--on-surface-variant)' }}>Risk not found</h2>
        <button className="btn-primary" onClick={() => navigate('/')} style={{ marginTop: '2rem' }}>
          Back to Dashboard
        </button>
      </main>
    );
  }

  const healthScore = risk.severity === 'high' ? 34 : risk.severity === 'medium' ? 58 : 78;

  // Simulated AI reasoning steps based on risk data
  const reasoningSteps = [
    {
      title: 'Pattern Detection',
      desc: `This risk was identified by the ${risk.source_agent || 'risk_spotter'} agent after analyzing current signals and OKR progress data.`,
    },
    {
      title: 'Severity Assessment',
      desc: `Classified as ${risk.severity?.toUpperCase()} severity. ${risk.description}`,
    },
    {
      title: 'Impact Projection',
      desc: `If unaddressed, this risk could impact related OKR targets and overall business health within the current quarter.`,
    },
  ];

  const strategyActions = [
    { priority: 'Critical', title: 'Immediate Review Required', desc: 'Schedule a focused review session to address this risk within the next 48 hours.' },
    { priority: 'High', title: 'Stakeholder Communication', desc: 'Brief relevant stakeholders on the current status and planned mitigation steps.' },
    { priority: 'Medium', title: 'Monitoring Protocol', desc: 'Set up automated monitoring to track changes in this risk metric on a daily basis.' },
  ];

  return (
    <main style={{ padding: '6rem 3rem 8rem 3rem', maxWidth: 1600, margin: '0 auto' }}>
      {/* Breadcrumb & Header */}
      <div className="animate-fade-up" style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '2rem' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span className="text-label">Signals</span>
            <span className="material-symbols-outlined" style={{ fontSize: '10px', color: 'var(--on-surface-variant)' }}>chevron_right</span>
            <span className="text-label" style={{ color: 'var(--secondary-fixed)' }}>Risk Analysis</span>
          </div>
          <h1 style={{
            fontFamily: 'var(--font-headline)',
            fontSize: 'clamp(2.5rem, 6vw, 5rem)',
            fontWeight: 800, letterSpacing: '-0.04em',
            lineHeight: 0.95, color: 'var(--primary)',
          }}>
            {risk.title.split(' — ')[0] || risk.title}
          </h1>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button className="btn-glow" style={{
            background: 'var(--surface-container-high)',
            boxShadow: 'none', color: 'var(--primary)',
          }}
          onClick={() => navigate('/')}>
            <span className="material-symbols-outlined">notifications_off</span>
            Dismiss
          </button>
          <button className="btn-glow" onClick={() => navigate('/')}>
            <span className="material-symbols-outlined">check_circle</span>
            Acknowledge
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="animate-fade-up-delay-1" style={{
        display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
        gap: '2rem', marginBottom: '6rem',
      }}>
        {/* Health Score */}
        <div className="card-tonal" style={{ textAlign: 'center', position: 'relative', padding: '3rem' }}>
          <div style={{
            position: 'absolute', inset: 0,
            background: 'linear-gradient(135deg, rgba(255,180,171,0.05), transparent)',
          }} />
          <div style={{ position: 'relative', zIndex: 1 }}>
            <p className="text-label" style={{ marginBottom: '2rem' }}>Health Score</p>
            <div style={{
              fontFamily: 'var(--font-headline)',
              fontSize: '7rem', fontWeight: 800,
              letterSpacing: '-0.04em',
              color: 'var(--error)', lineHeight: 1,
              marginBottom: '0.5rem',
            }}>
              {healthScore}
            </div>
            <div className="progress-track" style={{ maxWidth: 200, margin: '0 auto 1rem' }}>
              <div className="progress-fill danger" style={{ width: `${healthScore}%` }} />
            </div>
            <p style={{ color: 'var(--on-surface-variant)', fontSize: '0.875rem' }}>
              {healthScore < 40 ? 'Critical Threshold Breached' : healthScore < 60 ? 'Below Target' : 'Monitoring'}
            </p>
          </div>
        </div>

        {/* Deadline / Renewal */}
        <div className="card-tonal" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '3rem' }}>
          <div>
            <p className="text-label" style={{ marginBottom: '1rem' }}>Risk Identified</p>
            <h3 style={{
              fontFamily: 'var(--font-headline)',
              fontSize: '2.5rem', fontWeight: 700,
              color: 'var(--primary)', letterSpacing: '-0.02em',
            }}>
              {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </h3>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '2rem' }}>
            <span style={{ color: 'var(--on-surface-variant)', fontSize: '0.875rem' }}>Detected By</span>
            <span style={{ color: 'var(--primary)', fontWeight: 700, fontSize: '1rem' }}>
              {risk.source_agent || 'risk_spotter'}
            </span>
          </div>
        </div>

        {/* Risk Exposure */}
        <div className="card-tonal" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '3rem' }}>
          <div>
            <p className="text-label" style={{ marginBottom: '1rem' }}>Risk Exposure</p>
            <h3 style={{
              fontFamily: 'var(--font-headline)',
              fontSize: '2.5rem', fontWeight: 700,
              color: 'var(--primary)', letterSpacing: '-0.02em',
              textTransform: 'capitalize',
            }}>
              {risk.severity}
            </h3>
          </div>
        </div>
      </div>

      {/* Deep Dive Bento: AI Reasoning + Strategy */}
      <div className="animate-fade-up-delay-2" style={{
        display: 'grid', gridTemplateColumns: '7fr 5fr',
        gap: '3rem',
      }}>
        {/* AI Reasoning */}
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
            <span className="material-symbols-outlined" style={{ color: 'var(--secondary-container)' }}>psychology</span>
            <h2 className="text-headline-lg">AI Analysis Chain</h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
            {reasoningSteps.map((step, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '1.5rem' }}>
                <div style={{
                  color: 'var(--on-surface-variant)',
                  fontFamily: 'var(--font-headline)',
                  fontSize: '1.25rem', marginTop: '0.25rem',
                  minWidth: '2rem',
                }}>
                  {String(i + 1).padStart(2, '0')}
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  <h4 style={{ color: 'var(--primary)', fontWeight: 700, fontSize: '1.25rem' }}>
                    {step.title}
                  </h4>
                  <p style={{ color: 'var(--on-surface-variant)', lineHeight: 1.6 }}>
                    {step.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Strategy Response */}
        <div className="card-elevated">
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2.5rem' }}>
            <span className="material-symbols-outlined" style={{ color: 'var(--secondary-fixed)' }}>verified</span>
            <h2 style={{
              fontFamily: 'var(--font-headline)',
              fontSize: '1.5rem', fontWeight: 700, letterSpacing: '-0.01em',
            }}>
              Strategy Response
            </h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            {strategyActions.map((action, i) => (
              <div key={i} style={{
                background: 'var(--surface-container)', padding: '1.5rem',
                borderRadius: '0.75rem', cursor: 'pointer',
                transition: 'background 0.3s',
              }}
              onMouseEnter={(e) => e.currentTarget.style.background = 'var(--surface-bright)'}
              onMouseLeave={(e) => e.currentTarget.style.background = 'var(--surface-container)'}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span style={{
                    fontSize: '10px', textTransform: 'uppercase',
                    letterSpacing: '0.15em', fontWeight: 700,
                    color: action.priority === 'Critical' ? 'var(--secondary-fixed)' : 'var(--on-surface-variant)',
                  }}>
                    Priority: {action.priority}
                  </span>
                  <span className="material-symbols-outlined" style={{ fontSize: '0.875rem', color: 'var(--on-surface-variant)' }}>
                    arrow_forward
                  </span>
                </div>
                <h5 style={{ color: 'var(--primary)', fontWeight: 700, marginBottom: '0.5rem' }}>
                  {action.title}
                </h5>
                <p style={{ color: 'var(--on-surface-variant)', fontSize: '0.875rem', lineHeight: 1.4 }}>
                  {action.desc}
                </p>
              </div>
            ))}
          </div>

          <button
            className="btn-aurora"
            onClick={() => navigate('/')}
            style={{
              width: '100%', marginTop: '2.5rem',
              padding: '1rem', fontWeight: 700,
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
            }}
          >
            Commit to Recommended Plan
          </button>
        </div>
      </div>
    </main>
  );
}

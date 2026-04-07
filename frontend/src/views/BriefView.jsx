import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { generateBrief } from '../api';

export default function BriefView({ data, onRefresh }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [briefResult, setBriefResult] = useState(location.state?.briefResult || null);
  const [generating, setGenerating] = useState(false);

  // When CommandBar navigates here with a fresh result, pick it up
  useEffect(() => {
    if (location.state?.briefResult) {
      setBriefResult(location.state.briefResult);
      if (onRefresh) onRefresh();
    }
  }, [location.state]);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const result = await generateBrief();
      setBriefResult(result);
      onRefresh();
    } catch (err) {
      console.error('Failed to generate brief:', err);
    } finally {
      setGenerating(false);
    }
  };

  const briefText = briefResult?.brief || data?.latest_brief?.brief_text;
  const risks = data?.risks || [];
  const signals = data?.signals || [];

  return (
    <main style={{ marginLeft: 0, minHeight: '100vh', padding: '8rem 3rem 8rem 6rem', maxWidth: 1400 }}>
      {/* Breadcrumb & Header */}
      <header className="animate-fade-up" style={{ marginBottom: '6rem', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <nav>
          <button
            onClick={() => navigate('/')}
            style={{
              background: 'none', border: 'none',
              color: 'var(--on-surface-variant)', fontSize: '0.875rem',
              display: 'flex', alignItems: 'center', gap: '0.5rem',
              cursor: 'pointer', transition: 'color 0.3s',
            }}
          >
            <span className="material-symbols-outlined" style={{ fontSize: '0.875rem' }}>arrow_back</span>
            Back to Overview
          </button>
        </nav>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '2rem' }}>
          <h1 style={{
            fontFamily: 'var(--font-headline)',
            fontSize: 'clamp(3rem, 5vw, 4.5rem)',
            fontWeight: 800, letterSpacing: '-0.04em',
            lineHeight: 0.9, color: 'var(--primary)', maxWidth: '48rem',
          }}>
            Intelligence Brief
            <span style={{ display: 'block', color: 'var(--secondary-fixed-dim)' }}>
              {briefResult ? `#${Date.now().toString(36).toUpperCase().slice(-5)}` : 'Latest'}
            </span>
          </h1>

          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.5rem' }}>
            <span className="text-label">Generation Timestamp</span>
            <span style={{ fontWeight: 700, color: 'var(--primary)' }}>
              {briefResult ? new Date().toLocaleString('en-US', {
                month: 'short', day: 'numeric', year: 'numeric',
                hour: '2-digit', minute: '2-digit',
              }).toUpperCase() : data?.latest_brief?.generated_at
                ? new Date(data.latest_brief.generated_at).toLocaleString('en-US', {
                    month: 'short', day: 'numeric', year: 'numeric',
                    hour: '2-digit', minute: '2-digit',
                  }).toUpperCase()
                : 'NOT YET GENERATED'}
            </span>
          </div>
        </div>
      </header>

      {/* Generate Button */}
      {!briefText && !generating && (
        <section className="animate-fade-up-delay-1" style={{ marginBottom: '4rem', textAlign: 'center' }}>
          <button className="btn-aurora" onClick={handleGenerate} style={{ padding: '1rem 2.5rem', fontSize: '1rem' }}>
            <span className="material-symbols-outlined" style={{ verticalAlign: 'middle', marginRight: 8 }}>bolt</span>
            Synthesize Intelligence
          </button>
        </section>
      )}

      {generating && (
        <section className="animate-fade-up" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', padding: '4rem' }}>
          <div className="spinner" />
          <p style={{ color: 'var(--on-surface-variant)', fontSize: '0.875rem' }}>
            AI analysts scanning intelligence sources...
          </p>
        </section>
      )}

      {/* The Bottom Line */}
      {briefText && (
        <>
          <section className="animate-fade-up-delay-1" style={{ marginBottom: '8rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '3rem' }}>
              <span style={{ height: 1, width: '3rem', background: 'var(--outline-variant)', opacity: 0.3 }} />
              <h2 className="text-label">Executive Summary</h2>
            </div>

            <div style={{
              fontFamily: 'var(--font-headline)',
              fontSize: 'clamp(1.5rem, 3vw, 2.5rem)',
              lineHeight: 1.3, color: 'var(--primary)',
              maxWidth: '56rem', letterSpacing: '-0.02em',
            }}>
              <ReactMarkdown
                components={{
                  p: ({ children }) => <p style={{ marginBottom: '1rem' }}>{children}</p>,
                  h2: ({ children }) => <h2 style={{
                    fontFamily: 'var(--font-headline)', fontSize: '1.5rem',
                    fontWeight: 700, marginTop: '3rem', marginBottom: '1rem',
                    color: 'var(--primary)',
                  }}>{children}</h2>,
                  h3: ({ children }) => <h3 style={{
                    fontFamily: 'var(--font-headline)', fontSize: '1.25rem',
                    fontWeight: 700, marginTop: '2rem', marginBottom: '0.75rem',
                    color: 'var(--secondary-fixed-dim)',
                  }}>{children}</h3>,
                  li: ({ children }) => <li style={{
                    fontSize: '1rem', fontFamily: 'var(--font-body)',
                    color: 'var(--on-surface-variant)', lineHeight: 1.6,
                    marginBottom: '0.5rem',
                  }}>{children}</li>,
                  ul: ({ children }) => <ul style={{ paddingLeft: '1.5rem', marginBottom: '1rem' }}>{children}</ul>,
                  ol: ({ children }) => <ol style={{ paddingLeft: '1.5rem', marginBottom: '1rem' }}>{children}</ol>,
                  strong: ({ children }) => <strong style={{ color: 'var(--primary)', fontWeight: 700 }}>{children}</strong>,
                }}
              >
                {briefText}
              </ReactMarkdown>
            </div>

            {/* Brief meta stats */}
            {briefResult && (
              <div style={{
                display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
                gap: '4rem', marginTop: '2rem',
              }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <p style={{ fontSize: '1.875rem', fontWeight: 700, fontFamily: 'var(--font-headline)' }}>
                    {(briefResult.elapsed_ms / 1000).toFixed(2)}s
                  </p>
                  <p style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)' }}>
                    Synthesis latency
                  </p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <p style={{ fontSize: '1.875rem', fontWeight: 700, fontFamily: 'var(--font-headline)' }}>
                    {briefResult.health}
                  </p>
                  <p style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)' }}>
                    Portfolio health
                  </p>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <p style={{
                    fontSize: '1.875rem', fontWeight: 700,
                    fontFamily: 'var(--font-headline)',
                    color: briefResult.health === 'RED' ? 'var(--error)' : 'var(--primary)',
                  }}>
                    {briefResult.risk_count} Risks
                  </p>
                  <p style={{ fontSize: '0.75rem', color: 'var(--on-surface-variant)' }}>
                    Active risk flags
                  </p>
                </div>
              </div>
            )}
          </section>

          {/* Emerging Threats sidebar */}
          <div style={{
            display: 'grid', gridTemplateColumns: '1fr 1fr',
            gap: '3rem',
          }}>
            {/* Priority Actions */}
            <section className="animate-fade-up-delay-2">
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <span style={{ height: 1, width: '3rem', background: 'var(--outline-variant)', opacity: 0.3 }} />
                <h2 className="text-label">Recommended Actions</h2>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '3rem' }}>
                {risks.slice(0, 3).map((risk, i) => (
                  <div key={risk.id || i} style={{
                    display: 'flex', gap: '2rem', alignItems: 'flex-start',
                    transition: 'transform 0.5s', cursor: 'pointer',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.transform = 'translateX(8px)'}
                  onMouseLeave={(e) => e.currentTarget.style.transform = 'translateX(0)'}
                  >
                    <span style={{
                      fontSize: '3rem', fontWeight: 900,
                      color: 'rgba(58, 57, 57, 0.5)',
                      fontFamily: 'var(--font-headline)',
                      lineHeight: 1,
                    }}>
                      {String(i + 1).padStart(2, '0')}
                    </span>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      <h3 style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--primary)' }}>
                        {risk.title}
                      </h3>
                      <p style={{
                        color: 'var(--on-surface-variant)', lineHeight: 1.6,
                        maxWidth: '32rem',
                      }}>
                        {risk.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Emerging Threats */}
            <section className="animate-fade-up-delay-3">
              <div className="card-tonal" style={{ border: '1px solid rgba(59, 73, 75, 0.1)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                  <span style={{
                    width: 12, height: 12, borderRadius: '50%',
                    background: 'var(--error)',
                    boxShadow: '0 0 12px rgba(255,180,171,0.5)',
                  }} className="animate-pulse-dot" />
                  <h2 className="text-label">Emerging Threats</h2>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem' }}>
                  {signals.slice(0, 2).map((signal, i) => (
                    <div key={signal.id || i} style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                        <span style={{
                          color: signal.severity === 'high' ? 'var(--error)' : 'var(--on-surface-variant)',
                          fontSize: '0.75rem', fontWeight: 700,
                          textTransform: 'uppercase', letterSpacing: '0.1em',
                        }}>
                          {signal.signal_type?.replace('_', ' ')}
                        </span>
                      </div>
                      <h4 style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--primary)' }}>
                        {signal.subject}
                      </h4>
                      <p style={{ fontSize: '0.875rem', color: 'var(--on-surface-variant)', lineHeight: 1.6 }}>
                        {signal.summary}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </div>

          {/* Regenerate button */}
          <div style={{ textAlign: 'center', margin: '6rem 0' }}>
            <button className="btn-aurora" onClick={handleGenerate} disabled={generating}>
              {generating ? 'Synthesizing...' : 'Resynthesize'}
            </button>
          </div>
        </>
      )}
    </main>
  );
}

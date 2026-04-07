export default function HealthOrb({ health }) {
  const isRed = health === 'RED';
  const isAmber = health === 'AMBER';

  const orbBg = isRed
    ? 'linear-gradient(135deg, #ff6b6b, #ffb4ab)'
    : isAmber
    ? 'linear-gradient(135deg, #fbbf24, #f59e0b)'
    : 'linear-gradient(135deg, var(--secondary-container), var(--secondary))';

  const glowColor = isRed
    ? 'rgba(255, 180, 171, 0.2)'
    : isAmber
    ? 'rgba(251, 191, 36, 0.2)'
    : 'rgba(0, 238, 252, 0.2)';

  return (
    <div style={{ position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '5rem' }}>
      {/* Breathing glow background */}
      <div
        className="breathing-glow"
        style={{
          position: 'absolute',
          width: '16rem', height: '16rem',
          background: isRed ? 'var(--error)' : 'var(--secondary-container)',
          opacity: 0.2,
          filter: 'blur(120px)',
          borderRadius: '50%',
        }}
      />
      {/* Orb */}
      <div
        className="breathing-orb"
        style={{
          position: 'relative',
          width: '12rem', height: '12rem',
          borderRadius: '50%',
          background: orbBg,
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center',
          color: 'var(--on-secondary)',
          boxShadow: `0 0 120px ${glowColor}`,
        }}
      >
        <span style={{
          fontFamily: 'var(--font-headline)',
          fontSize: '3rem', fontWeight: 900,
          letterSpacing: '-0.04em',
        }}>
          {health || 'GREEN'}
        </span>
        <span style={{
          fontSize: '10px', textTransform: 'uppercase',
          letterSpacing: '0.15em', fontWeight: 700, opacity: 0.7,
        }}>
          Health Status
        </span>
      </div>
    </div>
  );
}

import HealthOrb from '../components/HealthOrb';
import StatsRow from '../components/StatsRow';
import OKRProgress from '../components/OKRProgress';
import CriticalSignals from '../components/CriticalSignals';
import RiskLandscape from '../components/RiskLandscape';
import CommandBar from '../components/CommandBar';

export default function DashboardView({ data }) {
  const health = data?.latest_brief?.health || 'GREEN';
  const risks = data?.risks || [];
  const signals = data?.signals || [];
  const okrs = data?.okrs || [];

  const healthText = {
    RED: 'Portfolio Review Required',
    AMBER: 'Elevated Monitoring Active',
    GREEN: 'All Clear — Portfolio Healthy',
  };

  const healthDesc = {
    RED: `${risks.length} risk flags raised requiring immediate executive review.`,
    AMBER: `${risks.length} flags being monitored. Some areas need your attention this week.`,
    GREEN: 'No critical flags. All portfolio metrics within target ranges.',
  };

  return (
    <main className="main-content">
      {/* Hero Section: Health Indicator */}
      <section className="animate-fade-up" style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        gap: '3rem', marginBottom: '6rem', flexWrap: 'wrap',
      }}>
        <div style={{ maxWidth: '40rem' }}>
          <h2 className="text-label" style={{ marginBottom: '1rem' }}>Portfolio Intelligence</h2>
          <h1 className="text-headline-xl" style={{ marginBottom: '2rem' }}>
            {healthText[health] || healthText.GREEN}
          </h1>
          <p style={{
            color: 'var(--on-surface-variant)', fontSize: '1.125rem',
            maxWidth: '28rem', lineHeight: 1.6,
          }}>
            {healthDesc[health] || healthDesc.GREEN}
          </p>
        </div>
        <HealthOrb health={health} />
      </section>

      {/* Stats Row */}
      <section className="animate-fade-up-delay-1">
        <StatsRow
          riskCount={risks.length}
          signalCount={signals.length}
          okrCount={okrs.length}
        />
      </section>

      {/* Bento Grid: OKR + Signals */}
      <section className="animate-fade-up-delay-2" style={{
        display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)',
        gap: '2rem', marginBottom: '2rem',
      }}>
        <OKRProgress okrs={okrs} />
        <CriticalSignals signals={signals} />
      </section>

      {/* Risk Landscape */}
      <section className="animate-fade-up-delay-3" style={{
        display: 'grid', gridTemplateColumns: '1fr',
        gap: '2rem', marginBottom: '6rem',
      }}>
        <RiskLandscape risks={risks} />
      </section>

      {/* Floating Command Bar */}
      <CommandBar />
    </main>
  );
}

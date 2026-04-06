import { NavLink, useNavigate } from 'react-router-dom';

export default function TopNav() {
  const navigate = useNavigate();

  return (
    <header className="top-nav">
      <div className="top-nav-inner">
        <div className="nav-brand" onClick={() => navigate('/')} style={{ cursor: 'pointer' }}>
          Vantage Point
        </div>

        <nav className="nav-links">
          <NavLink to="/" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            Dashboard
          </NavLink>
          <NavLink to="/brief" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            Strategy Hub
          </NavLink>
        </nav>

        <div className="nav-actions">
          <button className="btn-aurora" onClick={() => navigate('/brief')}>
            Synthesize Intelligence
          </button>
          <div style={{
            width: 40, height: 40, borderRadius: '50%',
            background: 'var(--surface-container-highest)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '0.75rem', fontWeight: 700, color: 'var(--on-surface-variant)',
          }}>
            VP
          </div>
        </div>
      </div>
    </header>
  );
}

import { useState, useEffect, useCallback } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { fetchDashboardData } from './api';
import TopNav from './components/TopNav';
import Footer from './components/Footer';
import DashboardView from './views/DashboardView';
import BriefView from './views/BriefView';
import RiskDetailView from './views/RiskDetailView';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = useCallback(async () => {
    try {
      setError(null);
      const result = await fetchDashboardData();
      setData(result);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Unable to connect to the Vantage Point API. Make sure the backend is running on port 8001.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, [loadData]);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p style={{ color: 'var(--on-surface-variant)', fontSize: '0.875rem' }}>
          Initializing Vantage Point...
        </p>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <TopNav />
      <Footer />
      {error && (
        <div style={{
          position: 'fixed', top: '5rem', left: '50%', transform: 'translateX(-50%)',
          background: 'var(--error-container)', color: 'var(--error)',
          padding: '0.75rem 1.5rem', borderRadius: '0.375rem', zIndex: 100,
          fontSize: '0.85rem', fontWeight: 600, maxWidth: '600px', textAlign: 'center',
        }}>
          {error}
        </div>
      )}
      <Routes>
        <Route path="/" element={<DashboardView data={data} onRefresh={loadData} />} />
        <Route path="/brief" element={<BriefView data={data} onRefresh={loadData} />} />
        <Route path="/risk/:riskId" element={<RiskDetailView data={data} onRefresh={loadData} />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;

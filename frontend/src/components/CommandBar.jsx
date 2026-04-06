import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { askQuestion } from '../api';

export default function CommandBar() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || loading) return;

    setLoading(true);
    try {
      await askQuestion(query);
      setQuery('');
      navigate('/brief');
    } catch (err) {
      console.error('Ask failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="command-bar">
      <form className="command-bar-inner" onSubmit={handleSubmit}>
        <span className="material-symbols-outlined" style={{ color: 'var(--secondary-fixed-dim)' }}>search</span>
        <input
          className="command-bar-input"
          type="text"
          placeholder="Ask your AI analyst anything..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
        />
        <button type="submit" className="command-bar-send" disabled={loading}>
          {loading ? 'Analyzing...' : 'Ask'}
          <span className="material-symbols-outlined" style={{ fontSize: '1.125rem' }}>send</span>
        </button>
      </form>
    </div>
  );
}

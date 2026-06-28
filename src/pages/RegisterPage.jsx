import React from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';
import { parseError, sleep } from '../utils/helpers';
import { CheckSquare } from 'lucide-react';
import Toast from '../components/Toast';
const RegisterPage = () => {
  const [displayName, setDisplayName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const [toast, setToast] = React.useState(null);
  const navigate = useNavigate();
  const handleSubmit = async e => {
    e.preventDefault();
    if (password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await API.post('/auth/signup', { email, password, display_name: displayName });
      const res = await API.post('/auth/login', { email, password });
      localStorage.setItem('token', res.data.access_token);
      if (res.data.display_name) localStorage.setItem('display_name', res.data.display_name);
      if (res.data.user_id) localStorage.setItem('user_id', String(res.data.user_id));
      if (res.data.email) localStorage.setItem('user_email', res.data.email);
      setToast({ msg: 'Account created!', type: 'success' });
      navigate('/dashboard');
    } catch (err) {
      const msg = parseError(err);
      setError(msg || 'Failed to register.');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 mx-auto mb-3 flex items-center justify-center">
            <span className="text-white font-bold text-xl">A</span>
          </div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Create account</h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">Join us today</p>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 p-6 space-y-4">
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Display Name</label>
            <input type="text" value={displayName} onChange={e => setDisplayName(e.target.value)} placeholder="e.g. John Smith" className="input" />
          </div>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Email</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" className="input" />
          </div>
          <div className="space-y-1">
            <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Password</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" className="input" />
            <p className="text-xs text-slate-400">Must be at least 8 characters</p>
          </div>
          <button type="submit" onClick={handleSubmit} disabled={loading || !displayName || !email || !password} className="btn-primary w-full justify-center flex items-center gap-1.5">
            {loading ? <CheckSquare size={16} className="animate-spin" /> : null}
            Sign Up
          </button>
        </div>
        <Toast toast={toast} />
      </div>
    </div>
  );
};
export default RegisterPage;
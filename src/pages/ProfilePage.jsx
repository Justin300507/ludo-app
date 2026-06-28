import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import API from '../api';
import { CheckSquare } from 'lucide-react';
const ProfilePage = () => {
  const [user, setUser] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [displayName, setDisplayName] = React.useState('');
  const [avatarUrl, setAvatarUrl] = React.useState('');
  const [saving, setSaving] = React.useState(false);
  const [toast, setToast] = React.useState(null);
  React.useEffect(() => {
    const fetchUser = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        const res = await API.get(`/users/${userId}`);
        setUser(res.data);
        setDisplayName(res.data.username);
        setAvatarUrl(res.data.avatar_url || '');
      } catch (err) {
        setToast({ msg: 'Failed to load profile', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);
  const handleSave = async () => {
    setSaving(true);
    try {
      await API.put(`/users/${user.id}`, { username: displayName, avatar_url: avatarUrl });
      setToast({ msg: 'Profile updated', type: 'success' });
    } catch (err) {
      setToast({ msg: 'Update failed', type: 'error' });
    } finally {
      setSaving(false);
    }
  };
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />
      <main className="ml-56 flex-1 p-6 overflow-auto">
        <Navbar />
        {loading ? (
          <LoadingSkeleton count={3} />
        ) : (
          <div className="max-w-md mx-auto bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-100 dark:border-slate-700">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-white mb-4">Profile</h2>
            <div className="space-y-4">
              <div className="space-y-1">
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Display Name</label>
                <input type="text" value={displayName} onChange={e => setDisplayName(e.target.value)} placeholder="e.g. John Smith" className="input" />
              </div>
              <div className="space-y-1">
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300">Avatar URL</label>
                <input type="text" value={avatarUrl} onChange={e => setAvatarUrl(e.target.value)} placeholder="https://example.com/avatar.png" className="input" />
              </div>
              <div className="flex gap-2">
                <button onClick={handleSave} disabled={saving} className="btn-primary flex-1 flex items-center gap-1.5">
                  {saving ? <CheckSquare size={16} className="animate-spin" /> : null}
                  Save
                </button>
                <button onClick={() => { setDisplayName(user.username); setAvatarUrl(user.avatar_url || ''); }} className="flex-1 bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl px-4 py-2">
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
        <Toast toast={toast} />
      </main>
    </div>
  );
};
export default ProfilePage;
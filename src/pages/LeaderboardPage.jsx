import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import ListItemCard from '../components/ListItemCard';
import { Search, ListTodo } from 'lucide-react';
import API from '../api';
const LeaderboardPage = () => {
  const [entries, setEntries] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [search, setSearch] = React.useState('');
  const [toast, setToast] = React.useState(null);
  React.useEffect(() => {
    const fetchEntries = async () => {
      try {
        const res = await API.get('/leaderboard?limit=20');
        setEntries(res.data.items || []);
      } catch (err) {
        setToast({ msg: 'Failed to load leaderboard', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchEntries();
  }, []);
  const filtered = entries.filter(e => (e.username || '').toLowerCase().includes(search.toLowerCase()));
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />
      <main className="ml-56 flex-1 p-6 overflow-auto">
        <Navbar />
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Leaderboard</h2>
          <div className="flex items-center gap-2 border border-slate-300 dark:border-slate-600 rounded-md px-3 py-2">
            <Search size={16} className="text-slate-500" />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search username" className="bg-transparent focus:outline-none text-sm" />
          </div>
        </div>
        {loading ? (
          <LoadingSkeleton count={5} />
        ) : filtered.length === 0 ? (
          <div className="text-center py-10 text-slate-500 dark:text-slate-400">
            <ListTodo size={48} className="mx-auto mb-4" />
            No results found
          </div>
        ) : (
          <table className="w-full table-auto bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700">
            <thead>
              <tr className="text-left">
                <th className="px-4 py-2 text-slate-500 dark:text-slate-400">User</th>
                <th className="px-4 py-2 text-slate-500 dark:text-slate-400">Wins</th>
                <th className="px-4 py-2 text-slate-500 dark:text-slate-400">Losses</th>
                <th className="px-4 py-2 text-slate-500 dark:text-slate-400">Win Rate</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(entry => (
                <tr key={entry.user_id} className="border-t border-slate-100 dark:border-slate-700">
                  <td className="px-4 py-2">{entry.username || 'Anonymous'}</td>
                  <td className="px-4 py-2">{entry.wins}</td>
                  <td className="px-4 py-2">{entry.losses}</td>
                  <td className="px-4 py-2">{(entry.win_rate * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <Toast toast={toast} />
      </main>
    </div>
  );
};
export default LeaderboardPage;
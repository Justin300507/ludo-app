import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import ListItemCard from '../components/ListItemCard';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import { Search, ListTodo, Plus } from 'lucide-react';
import API from '../api';
const LobbyListPage = () => {
  const [lobbies, setLobbies] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [search, setSearch] = React.useState('');
  const [filter, setFilter] = React.useState('all');
  const [toast, setToast] = React.useState(null);
  React.useEffect(() => {
    const fetchLobbies = async () => {
      try {
        const res = await API.get('/games?limit=20');
        setLobbies(res.data.items || []);
      } catch (err) {
        setToast({ msg: 'Failed to load lobbies', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchLobbies();
  }, []);
  const filtered = lobbies.filter(l => {
    const matchesSearch = l.lobby_code.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === 'all' || (filter === 'open' && l.status === 'open') || (filter === 'closed' && l.status === 'closed');
    return matchesSearch && matchesFilter;
  });
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />
      <main className="ml-56 flex-1 p-6 overflow-auto">
        <Navbar />
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Lobbies</h2>
          <button className="btn-primary flex items-center gap-1.5"><Plus size={16} /> Add Lobby</button>
        </div>
        <div className="flex gap-4 mb-4">
          <div className="flex items-center gap-2 border border-slate-300 dark:border-slate-600 rounded-md px-3 py-2">
            <Search size={16} className="text-slate-500" />
            <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search lobby code" className="bg-transparent focus:outline-none text-sm" />
          </div>
          <select value={filter} onChange={e => setFilter(e.target.value)} className="input">
            <option value="all">All</option>
            <option value="open">Open</option>
            <option value="closed">Closed</option>
          </select>
        </div>
        {loading ? (
          <LoadingSkeleton count={5} />
        ) : filtered.length === 0 ? (
          <div className="text-center py-10 text-slate-500 dark:text-slate-400">
            <ListTodo size={48} className="mx-auto mb-4" />
            No results found
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map(lobby => (
              <ListItemCard
                key={lobby.id}
                icon={<ListTodo size={18} className="text-indigo-600" />}
                title={`Lobby ${lobby.lobby_code}`}
                subtitle={`Status: ${lobby.status} • ${lobby.is_private ? 'Private' : 'Public'}`}
                trailing={lobby.players_count ? `${lobby.players_count} players` : null}
              />
            ))}
          </div>
        )}
        <Toast toast={toast} />
      </main>
    </div>
  );
};
export default LobbyListPage;
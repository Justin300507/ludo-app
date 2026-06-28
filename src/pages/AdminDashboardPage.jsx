import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import ListItemCard from '../components/ListItemCard';
import { Users, Trash2, Plus, Search } from 'lucide-react';
import API from '../api';
const AdminDashboardPage = () => {
  const [users, setUsers] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [search, setSearch] = React.useState('');
  const [toast, setToast] = React.useState(null);
  React.useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await API.get('/users?limit=20');
        setUsers(res.data.items || []);
      } catch (err) {
        setToast({ msg: 'Failed to load users', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);
  const filtered = users.filter(u => u.username.toLowerCase().includes(search.toLowerCase()));
  const handleDelete = async id => {
    try {
      await API.delete(`/users/${id}`);
      setUsers(prev => prev.filter(u => u.id !== id));
      setToast({ msg: 'User deleted', type: 'success' });
    } catch (err) {
      setToast({ msg: 'Delete failed', type: 'error' });
    }
  };
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />
      <main className="ml-56 flex-1 p-6 overflow-auto">
        <Navbar />
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">User Management</h2>
          <button className="btn-primary flex items-center gap-1.5"><Plus size={16} /> Add User</button>
        </div>
        <div className="flex items-center gap-2 border border-slate-300 dark:border-slate-600 rounded-md px-3 py-2 mb-4">
          <Search size={16} className="text-slate-500" />
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search username" className="bg-transparent focus:outline-none text-sm" />
        </div>
        {loading ? (
          <LoadingSkeleton count={5} />
        ) : filtered.length === 0 ? (
          <div className="text-center py-10 text-slate-500 dark:text-slate-400">
            <Users size={48} className="mx-auto mb-4" />
            No results found
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map(user => (
              <ListItemCard
                key={user.id}
                icon={<Users size={18} className="text-indigo-600" />}
                title={user.username}
                subtitle={user.email}
                trailing={<Trash2 size={16} className="text-red-600 cursor-pointer" onClick={() => handleDelete(user.id)} />}
              />
            ))}
          </div>
        )}
        <Toast toast={toast} />
      </main>
    </div>
  );
};
export default AdminDashboardPage;
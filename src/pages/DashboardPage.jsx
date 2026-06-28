import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import StatCard from '../components/StatCard';
import { CheckSquare, Calendar, Clock, Target, MessageSquare } from 'lucide-react';
import API from '../api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
const DashboardPage = () => {
  const [stats, setStats] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [toast, setToast] = React.useState(null);
  React.useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await API.get('/stats/summary');
        setStats(res.data);
      } catch (err) {
        setToast({ msg: 'Failed to load stats', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);
  const chartData = [
    { month: 'Jan', total: 840 },
    { month: 'Feb', total: 720 },
    { month: 'Mar', total: 1100 },
    { month: 'Apr', total: 890 },
    { month: 'May', total: 1240 },
    { month: 'Jun', total: 980 },
  ];
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />
      <main className="ml-56 flex-1 p-6 overflow-auto">
        <Navbar />
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Hello, {localStorage.getItem('display_name') || 'User'}</h2>
          <p className="text-slate-500 dark:text-slate-400">{new Date().toLocaleDateString()}</p>
        </div>
        {loading ? (
          <LoadingSkeleton count={4} />
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <StatCard label="Total Users" value={stats?.total_users || 0} icon={<CheckSquare size={18} className="text-indigo-600" />} changeText="+5% this week" changeColor="text-indigo-600" />
            <StatCard label="Active Games" value={stats?.active_games || 0} icon={<Target size={18} className="text-indigo-600" />} changeText="+2% today" changeColor="text-indigo-600" />
            <StatCard label="Messages Sent" value={stats?.messages_sent || 0} icon={<MessageSquare size={18} className="text-indigo-600" />} changeText="+12% month" changeColor="text-indigo-600" />
            <StatCard label="Leaderboard Updates" value={stats?.leaderboard_updates || 0} icon={<Calendar size={18} className="text-indigo-600" />} changeText="+8% week" changeColor="text-indigo-600" />
          </div>
        )}
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-5">
          <h3 className="font-semibold text-slate-900 dark:text-white mb-4">Monthly Overview</h3>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="month" tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fontSize: 12, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e293b', border: 'none', borderRadius: '8px', color: '#f1f5f9' }} />
              <Area type="monotone" dataKey="total" stroke="#6366f1" strokeWidth={2} fill="url(#colorTotal)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <Toast toast={toast} />
      </main>
    </div>
  );
};
export default DashboardPage;
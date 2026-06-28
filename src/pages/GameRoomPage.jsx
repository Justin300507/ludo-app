import React from 'react';
import Sidebar from '../components/Sidebar';
import Navbar from '../components/Navbar';
import LoadingSkeleton from '../components/LoadingSkeleton';
import Toast from '../components/Toast';
import { CheckSquare } from 'lucide-react';
import API from '../api';
const GameRoomPage = () => {
  const [game, setGame] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [toast, setToast] = React.useState(null);
  const gameId = window.location.pathname.split('/').pop();
  React.useEffect(() => {
    const fetchGame = async () => {
      try {
        const res = await API.get(`/games/${gameId}`);
        setGame(res.data);
      } catch (err) {
        setToast({ msg: 'Failed to load game', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchGame();
  }, [gameId]);
  return (
    <div className="flex min-h-screen bg-slate-50 dark:bg-slate-900">
      <Sidebar />
      <main className="ml-56 flex-1 p-6 overflow-auto">
        <Navbar />
        {loading ? (
          <LoadingSkeleton count={3} />
        ) : (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold text-slate-900 dark:text-white">Game {game.lobby_code}</h2>
            <div className="flex items-center gap-4">
              <span className="px-3 py-1 bg-indigo-50 dark:bg-indigo-900/30 rounded-full text-indigo-600">{game.status}</span>
              <button className="btn-primary flex items-center gap-1.5"><CheckSquare size={16} /> Ready</button>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700">
              <p className="text-slate-500 dark:text-slate-400">Chat placeholder...</p>
            </div>
          </div>
        )}
        <Toast toast={toast} />
      </main>
    </div>
  );
};
export default GameRoomPage;
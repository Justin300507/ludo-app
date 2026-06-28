import React from 'react';
import { Sun, Moon, LogOut } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
const Navbar = () => {
  const [dark, setDark] = React.useState(document.documentElement.classList.contains('dark'));
  const navigate = useNavigate();
  const toggleDark = () => {
    setDark(d => !d);
    document.documentElement.classList.toggle('dark', !dark);
  };
  const handleLogout = () => {
    ['token','display_name','user_id','user_email'].forEach(k => localStorage.removeItem(k));
    navigate('/login');
  };
  return (
    <header className="flex justify-between items-center p-4 border-b border-slate-100 dark:border-slate-700">
      <h1 className="text-xl font-semibold text-slate-900 dark:text-white">Dashboard</h1>
      <div className="flex items-center gap-2">
        <button onClick={toggleDark} className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button onClick={handleLogout} className="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors">
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
};
export default Navbar;
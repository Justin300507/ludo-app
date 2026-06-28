import React from 'react';
const ListItemCard = ({ icon, title, subtitle, trailing }) => (
  <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-100 dark:border-slate-700 p-4 flex items-center justify-between hover:shadow-sm transition-shadow">
    <div className="flex items-center gap-3">
      <div className="w-9 h-9 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center">
        {icon}
      </div>
      <div>
        <p className="text-sm font-semibold text-slate-900 dark:text-white">{title}</p>
        <p className="text-xs text-slate-500 dark:text-slate-400">{subtitle}</p>
      </div>
    </div>
    {trailing && <span className="text-sm font-bold text-indigo-600">{trailing}</span>}
  </div>
);
export default ListItemCard;
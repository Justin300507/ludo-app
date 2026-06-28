import React from 'react';
const StatCard = ({ label, value, icon, changeText, changeColor }) => (
  <div className="bg-white dark:bg-slate-800 rounded-xl p-5 border border-slate-100 dark:border-slate-700 shadow-sm">
    <div className="flex items-center justify-between mb-3">
      <p className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wide">{label}</p>
      <div className="bg-indigo-50 dark:bg-indigo-900/30 p-2 rounded-lg">
        {icon}
      </div>
    </div>
    <p className="text-2xl font-bold text-slate-900 dark:text-white">{value}</p>
    {changeText && (
      <p className={`text-xs ${changeColor} mt-1 flex items-center gap-1`}>{changeText}</p>
    )}
  </div>
);
export default StatCard;
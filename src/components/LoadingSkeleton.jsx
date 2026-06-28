import React from 'react';
const LoadingSkeleton = ({ count = 5 }) => (
  <div className="animate-pulse space-y-3">
    {[...Array(count)].map((_, i) => (
      <div key={i} className="h-16 bg-slate-200 dark:bg-slate-700 rounded-xl" />
    ))}
  </div>
);
export default LoadingSkeleton;
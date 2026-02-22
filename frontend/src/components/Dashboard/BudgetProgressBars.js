import React from 'react';
import { formatINR } from '../../services/helpers';

function bar(pct) {
  const color = pct >= 85 ? 'bg-red-500' : pct >= 60 ? 'bg-yellow-500' : 'bg-green-500';
  return (
    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
      <div
        className={`${color} h-2.5 rounded-full transition-all duration-500`}
        style={{ width: `${Math.min(pct, 100)}%` }}
      />
    </div>
  );
}

export default function BudgetProgressBars({ budgets, breakdown }) {
  if (!budgets || !budgets.length) return null;

  return (
    <div className="card">
      <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">Budget Progress</h3>
      <div className="space-y-4">
        {budgets.map((b) => {
          const spent = b.category_id
            ? (breakdown || []).find(x => x.id === b.category_id)?.total || 0
            : 0;
          const pct = b.amount > 0 ? (spent / b.amount) * 100 : 0;
          return (
            <div key={b.id}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium text-gray-700 dark:text-gray-300">
                  {b.category_emoji} {b.category_name || 'Overall'}
                </span>
                <span className="text-gray-500 dark:text-gray-400">
                  {formatINR(spent)} / {formatINR(b.amount)}
                  {pct >= 85 && <span className="ml-1 text-red-500">⚠️</span>}
                </span>
              </div>
              {bar(pct)}
            </div>
          );
        })}
      </div>
    </div>
  );
}

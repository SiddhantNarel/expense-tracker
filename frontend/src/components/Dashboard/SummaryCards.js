import React from 'react';
import { formatINR } from '../../services/helpers';

function Card({ title, value, icon, color, sub }) {
  return (
    <div className="card flex items-start gap-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${color}`}>
        {icon}
      </div>
      <div>
        <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
        <p className="text-xl font-bold text-gray-900 dark:text-gray-100">{value}</p>
        {sub && <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{sub}</p>}
      </div>
    </div>
  );
}

export default function SummaryCards({ summary }) {
  if (!summary) return null;
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <Card
        title="Total Spent"
        value={formatINR(summary.total_expense)}
        icon="💸"
        color="bg-red-50 dark:bg-red-900/20"
      />
      <Card
        title="Total Income"
        value={formatINR(summary.total_income)}
        icon="💰"
        color="bg-green-50 dark:bg-green-900/20"
      />
      <Card
        title="Net Savings"
        value={formatINR(summary.net_savings)}
        icon="🏦"
        color="bg-blue-50 dark:bg-blue-900/20"
        sub={summary.net_savings >= 0 ? 'Great job! 🎉' : 'Over budget ⚠️'}
      />
      <Card
        title="Budget Remaining"
        value={formatINR(summary.budget_remaining)}
        icon="🎯"
        color="bg-purple-50 dark:bg-purple-900/20"
        sub={summary.overall_budget > 0 ? `of ${formatINR(summary.overall_budget)}` : 'No budget set'}
      />
    </div>
  );
}

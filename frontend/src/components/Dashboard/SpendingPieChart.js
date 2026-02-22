import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { formatINR } from '../../services/helpers';

export default function SpendingPieChart({ data }) {
  const filtered = (data || []).filter(d => d.total > 0);
  if (!filtered.length) {
    return (
      <div className="card">
        <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">Spending by Category</h3>
        <div className="flex items-center justify-center h-48 text-gray-400">No data</div>
      </div>
    );
  }
  return (
    <div className="card">
      <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">Spending by Category</h3>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={filtered}
            dataKey="total"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={90}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            labelLine={false}
          >
            {filtered.map((entry, i) => (
              <Cell key={i} fill={entry.color || '#6366f1'} />
            ))}
          </Pie>
          <Tooltip formatter={(v) => formatINR(v)} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

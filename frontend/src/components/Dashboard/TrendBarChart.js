import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { formatINR } from '../../services/helpers';

export default function TrendBarChart({ data }) {
  if (!data || !data.length) {
    return (
      <div className="card">
        <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">Spending Trends</h3>
        <div className="flex items-center justify-center h-48 text-gray-400">No data</div>
      </div>
    );
  }
  return (
    <div className="card">
      <h3 className="font-semibold text-gray-700 dark:text-gray-300 mb-4">Spending Trends</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="period" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} tickFormatter={(v) => `₹${v}`} />
          <Tooltip formatter={(v) => formatINR(v)} />
          <Bar dataKey="total" fill="#3b82f6" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

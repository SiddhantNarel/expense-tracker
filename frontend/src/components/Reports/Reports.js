import React, { useState } from 'react';
import { exportExpenses, exportIncome, exportLoans, exportReport } from '../../services/api';
import { getMonthStart, getToday } from '../../services/helpers';
import toast from 'react-hot-toast';

export default function Reports() {
  const [dateFrom, setDateFrom] = useState(getMonthStart());
  const [dateTo, setDateTo] = useState(getToday());

  const download = (url) => {
    window.open(url, '_blank');
    toast.success('Download started!');
  };

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">📈 Reports & Export</h2>

      <div className="card space-y-4">
        <h3 className="font-semibold text-gray-700 dark:text-gray-300">Date Range</h3>
        <div className="flex gap-3 flex-wrap">
          <div>
            <label className="label">From</label>
            <input type="date" className="input" value={dateFrom} onChange={e => setDateFrom(e.target.value)} />
          </div>
          <div>
            <label className="label">To</label>
            <input type="date" className="input" value={dateTo} onChange={e => setDateTo(e.target.value)} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="card space-y-3">
          <h3 className="font-semibold text-gray-700 dark:text-gray-300">💸 Expenses CSV</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Export all expenses for the selected date range</p>
          <button className="btn-primary w-full" onClick={() => download(exportExpenses({ from: dateFrom, to: dateTo }))}>
            ⬇ Download Expenses CSV
          </button>
        </div>
        <div className="card space-y-3">
          <h3 className="font-semibold text-gray-700 dark:text-gray-300">💰 Income CSV</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Export all income entries for the selected date range</p>
          <button className="btn-primary w-full" onClick={() => download(exportIncome({ from: dateFrom, to: dateTo }))}>
            ⬇ Download Income CSV
          </button>
        </div>
        <div className="card space-y-3">
          <h3 className="font-semibold text-gray-700 dark:text-gray-300">🤝 Loans CSV</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Export all loan transactions</p>
          <button className="btn-primary w-full" onClick={() => download(exportLoans())}>
            ⬇ Download Loans CSV
          </button>
        </div>
        <div className="card space-y-3">
          <h3 className="font-semibold text-gray-700 dark:text-gray-300">📊 Summary Report</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400">Full summary with income, expenses, categories, and savings</p>
          <button className="btn-primary w-full" onClick={() => download(exportReport({ from: dateFrom, to: dateTo }))}>
            ⬇ Download Report CSV
          </button>
        </div>
      </div>
    </div>
  );
}

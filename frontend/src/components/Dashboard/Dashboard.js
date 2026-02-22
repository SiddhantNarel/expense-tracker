import React, { useEffect, useState } from 'react';
import { getSummary, getCategoryBreakdown, getTrends, getBudgets } from '../../services/api';
import { getMonthStart, getToday } from '../../services/helpers';
import SummaryCards from './SummaryCards';
import SpendingPieChart from './SpendingPieChart';
import TrendBarChart from './TrendBarChart';
import BudgetProgressBars from './BudgetProgressBars';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [breakdown, setBreakdown] = useState([]);
  const [trends, setTrends] = useState([]);
  const [budgets, setBudgets] = useState([]);
  const [dateFrom, setDateFrom] = useState(getMonthStart());
  const [dateTo, setDateTo] = useState(getToday());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const params = { from: dateFrom, to: dateTo };
    const d = new Date(dateFrom);
    Promise.all([
      getSummary(params),
      getCategoryBreakdown(params),
      getTrends({ ...params, group_by: 'day' }),
      getBudgets({ month: d.getMonth() + 1, year: d.getFullYear() }),
    ]).then(([s, b, t, bu]) => {
      setSummary(s.data);
      setBreakdown(b.data);
      setTrends(t.data);
      setBudgets(bu.data);
    }).finally(() => setLoading(false));
  }, [dateFrom, dateTo]);

  return (
    <div className="p-6 space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Dashboard</h2>
        <div className="flex gap-2 items-center flex-wrap">
          <label className="text-sm text-gray-600 dark:text-gray-400">From</label>
          <input
            type="date"
            value={dateFrom}
            onChange={e => setDateFrom(e.target.value)}
            className="input w-auto"
          />
          <label className="text-sm text-gray-600 dark:text-gray-400">To</label>
          <input
            type="date"
            value={dateTo}
            onChange={e => setDateTo(e.target.value)}
            className="input w-auto"
          />
        </div>
      </div>
      {loading ? (
        <div className="flex items-center justify-center h-48">
          <div className="animate-spin text-3xl">⚙️</div>
        </div>
      ) : (
        <>
          <SummaryCards summary={summary} />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SpendingPieChart data={breakdown} />
            <TrendBarChart data={trends} />
          </div>
          <BudgetProgressBars budgets={budgets} breakdown={breakdown} />
        </>
      )}
    </div>
  );
}

import React, { useEffect, useState } from 'react';
import { getBudgets, deleteBudget, getCategories } from '../../services/api';
import { formatINR } from '../../services/helpers';
import toast from 'react-hot-toast';
import SetBudgetForm from './SetBudgetForm';

export default function BudgetList() {
  const [budgets, setBudgets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const d = new Date();
  const [month, setMonth] = useState(d.getMonth() + 1);
  const [year, setYear] = useState(d.getFullYear());

  const load = () => {
    getBudgets({ month, year }).then(r => setBudgets(r.data));
  };

  useEffect(() => {
    getCategories().then(r => setCategories(r.data));
  }, []);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { load(); }, [month, year]);

  const handleDelete = (id) => {
    if (!window.confirm('Delete this budget?')) return;
    deleteBudget(id).then(() => { toast.success('Deleted'); load(); });
  };

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Budgets</h2>
        <button className="btn-primary" onClick={() => setShowForm(true)}>+ Set Budget</button>
      </div>

      <div className="flex gap-3 items-center">
        <select className="input w-32" value={month} onChange={e => setMonth(Number(e.target.value))}>
          {Array.from({ length: 12 }, (_, i) => (
            <option key={i + 1} value={i + 1}>
              {new Date(2024, i, 1).toLocaleString('en-IN', { month: 'long' })}
            </option>
          ))}
        </select>
        <input type="number" className="input w-28" value={year} onChange={e => setYear(Number(e.target.value))} />
      </div>

      <div className="space-y-3">
        {budgets.length === 0 && <div className="card text-center text-gray-400 py-12">No budgets set</div>}
        {budgets.map(b => (
          <div key={b.id} className="card flex items-center justify-between gap-4">
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">
                {b.category_emoji} {b.category_name || 'Overall Budget'}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                {new Date(year, month - 1, 1).toLocaleString('en-IN', { month: 'long', year: 'numeric' })}
              </p>
            </div>
            <div className="flex items-center gap-3">
              <span className="font-bold text-blue-500">{formatINR(b.amount)}</span>
              <button className="btn-danger text-xs px-3 py-1.5" onClick={() => handleDelete(b.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>

      {showForm && (
        <SetBudgetForm
          categories={categories}
          month={month}
          year={year}
          onSave={() => { setShowForm(false); load(); }}
          onClose={() => setShowForm(false)}
        />
      )}
    </div>
  );
}

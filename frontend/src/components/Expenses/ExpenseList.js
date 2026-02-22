import React, { useEffect, useState } from 'react';
import { getExpenses, deleteExpense, getCategories } from '../../services/api';
import { formatINR } from '../../services/helpers';
import toast from 'react-hot-toast';
import AddExpenseForm from './AddExpenseForm';

export default function ExpenseList() {
  const [expenses, setExpenses] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ search: '', from: '', to: '', category_id: '', payment_method: '', sort_by: 'date', sort_order: 'desc' });

  const load = () => {
    setLoading(true);
    getExpenses({ ...filters, page, per_page: 15 })
      .then(res => {
        setExpenses(res.data.data);
        setTotal(res.data.total);
        setPages(res.data.pages);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => { getCategories().then(r => setCategories(r.data)); }, []);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { load(); }, [page, filters]);

  const handleDelete = (id) => {
    if (!window.confirm('Delete this expense?')) return;
    deleteExpense(id).then(() => { toast.success('Expense deleted'); load(); });
  };

  const handleSaved = () => { setShowForm(false); setEditing(null); load(); };

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-3">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">Expenses</h2>
        <button className="btn-primary" onClick={() => { setEditing(null); setShowForm(true); }}>
          + Add Expense
        </button>
      </div>

      {/* Filters */}
      <div className="card grid grid-cols-2 md:grid-cols-4 gap-3">
        <input placeholder="Search..." className="input" value={filters.search} onChange={e => setFilters(f => ({ ...f, search: e.target.value }))} />
        <input type="date" className="input" value={filters.from} onChange={e => setFilters(f => ({ ...f, from: e.target.value }))} />
        <input type="date" className="input" value={filters.to} onChange={e => setFilters(f => ({ ...f, to: e.target.value }))} />
        <select className="input" value={filters.category_id} onChange={e => setFilters(f => ({ ...f, category_id: e.target.value }))}>
          <option value="">All Categories</option>
          {categories.map(c => <option key={c.id} value={c.id}>{c.emoji} {c.name}</option>)}
        </select>
        <select className="input" value={filters.payment_method} onChange={e => setFilters(f => ({ ...f, payment_method: e.target.value }))}>
          <option value="">All Methods</option>
          {['Cash', 'GPay', 'Credit Card', 'Debit Card', 'Wallet'].map(m => <option key={m}>{m}</option>)}
        </select>
        <select className="input" value={`${filters.sort_by}_${filters.sort_order}`} onChange={e => { const [by, ord] = e.target.value.split('_'); setFilters(f => ({ ...f, sort_by: by, sort_order: ord })); }}>
          <option value="date_desc">Newest First</option>
          <option value="date_asc">Oldest First</option>
          <option value="amount_desc">High to Low</option>
          <option value="amount_asc">Low to High</option>
        </select>
      </div>

      <div className="text-sm text-gray-500 dark:text-gray-400">{total} expenses found</div>

      {loading ? (
        <div className="text-center py-10 text-gray-400">Loading...</div>
      ) : (
        <div className="space-y-2">
          {expenses.length === 0 && <div className="card text-center text-gray-400 py-12">No expenses yet</div>}
          {expenses.map(exp => (
            <div key={exp.id} className="card flex items-center justify-between gap-4 p-4">
              <div className="flex items-center gap-3">
                <span className="text-2xl">{exp.category_emoji || '📦'}</span>
                <div>
                  <p className="font-medium text-gray-900 dark:text-gray-100">{exp.description || exp.category_name || 'Expense'}</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">{exp.date} · {exp.payment_method} · {exp.category_name}</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="font-bold text-red-500 text-lg">{formatINR(exp.amount)}</span>
                <button className="btn-secondary text-xs px-3 py-1.5" onClick={() => { setEditing(exp); setShowForm(true); }}>Edit</button>
                <button className="btn-danger text-xs px-3 py-1.5" onClick={() => handleDelete(exp.id)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Pagination */}
      {pages > 1 && (
        <div className="flex gap-2 justify-center mt-4">
          <button className="btn-secondary px-3 py-1" disabled={page === 1} onClick={() => setPage(p => p - 1)}>←</button>
          <span className="py-1 text-sm text-gray-600 dark:text-gray-400">Page {page} of {pages}</span>
          <button className="btn-secondary px-3 py-1" disabled={page === pages} onClick={() => setPage(p => p + 1)}>→</button>
        </div>
      )}

      {showForm && (
        <AddExpenseForm
          expense={editing}
          categories={categories}
          onSave={handleSaved}
          onClose={() => { setShowForm(false); setEditing(null); }}
        />
      )}
    </div>
  );
}
